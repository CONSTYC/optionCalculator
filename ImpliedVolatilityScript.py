from PyQt5 import QtWidgets, QtGui, QtCore
from bin.PricingF import BSMImpVol, BAWImpVol
import sys
from datetime import datetime, timedelta


class IVThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal()

    def __init__(self, K, F, sigmai, r, T, q, OptionType, epsilon, opt):
        super(IVThread, self).__init__()
        self.K = K
        self.F = F
        self.sigmai = sigmai
        self.r = r
        self.T = T
        self.q = q
        self.OptionType = OptionType
        self.epsilon = epsilon
        self.opt = opt

    def run(self):
        try:
            self.BSMImpliedVol = round(BSMImpVol(
                self.K, self.F, self.sigmai, self.r, self.T, self.q, self.OptionType, self.opt
            ), 4)
            self.BAWImpliedVol = round(BAWImpVol(
                self.K, self.F, self.sigmai, self.r, self.T, self.q, self.OptionType, self.epsilon, self.opt
            ), 4)
            self.trigger.emit()
        except:
            print('IV Thread Run Error')


class ImpliedVolatilityWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ImpliedVolatilityWindow, self).__init__()

        self.initUI()

    def initUI(self):
        FontSize = 10
        Font_Label = '微软雅黑'

        self.StatusBar = self.statusBar()

        grid = QtWidgets.QGridLayout()
        ImpliedVol_Center = QtWidgets.QWidget()
        ImpliedVol_Center.setLayout(grid)
        self.setCentralWidget(ImpliedVol_Center)

        Input_Parameter_Text = [
            '行权价', '市价', '利率',
            '年天数', '股息率', 'BAW精度'
        ]
        self.strike = QtWidgets.QDoubleSpinBox()
        self.strike.setDecimals(2)
        self.strike.setSingleStep(0.01)
        self.strike.setMaximum(999999)
        self.strike.setValue(100)
        self.strike.setStatusTip('输入行权价格')

        self.price = QtWidgets.QDoubleSpinBox()
        self.price.setDecimals(2)
        self.price.setSingleStep(0.01)
        self.price.setMaximum(999999)
        self.price.setValue(100)
        self.price.setStatusTip('输入当前市价')

        # self.vol = QtWidgets.QLineEdit()
        # self.vol.setText('20')
        # self.vol.setStatusTip('输入波动率')

        self.rate = QtWidgets.QDoubleSpinBox()
        self.rate.setDecimals(4)
        self.rate.setSingleStep(0.0001)
        self.rate.setValue(0.03)
        self.rate.setStatusTip('输入无风险利率')

        self.ty = QtWidgets.QSpinBox()
        self.ty.setMaximum(366)
        self.ty.setValue(360)
        self.ty.setStatusTip('输入一年的天数')

        # self.maturity = QtWidgets.QLineEdit()
        # self.maturity.setText('30')
        # self.maturity.setStatusTip('输入期权期限')

        self.dividend = QtWidgets.QDoubleSpinBox()
        self.dividend.setDecimals(4)
        self.dividend.setSingleStep(0.0001)
        self.dividend.setValue(0.03)
        self.dividend.setStatusTip('输入股息率')

        self.epsilon = QtWidgets.QDoubleSpinBox()
        self.epsilon.setDecimals(7)
        self.epsilon.setValue(0.00001)
        self.epsilon.setSingleStep(0.0000001)
        self.epsilon.setStatusTip('输入BAW精度')

        Input_Parameter = [
            self.strike, self.price, self.rate,
            self.ty, self.dividend, self.epsilon
        ]
        strikeLabel = QtWidgets.QLabel('&K: ' + Input_Parameter_Text[0])
        priceLabel = QtWidgets.QLabel('&F: ' + Input_Parameter_Text[1])
        rateLabel = QtWidgets.QLabel('&r: ' + Input_Parameter_Text[2])
        tyLabel = QtWidgets.QLabel('&y: ' + Input_Parameter_Text[3])
        dividendLabel = QtWidgets.QLabel('&q: ' + Input_Parameter_Text[4])
        epsilonLabel = QtWidgets.QLabel('&e: ' + Input_Parameter_Text[5])
        Input_Parameter_Label = [
            strikeLabel, priceLabel, rateLabel,
            tyLabel, dividendLabel, epsilonLabel
        ]
        for i in range(len(Input_Parameter_Text)):
            Input_Parameter[i].setFixedWidth(140)
            Input_Parameter[i].setFont(QtGui.QFont(Font_Label, FontSize))
            # Input_Parameter[i].returnPressed.connect(self.OptionCalculate)
            Input_Parameter_Label[i].setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
            Input_Parameter_Label[i].setBuddy(Input_Parameter[i])
            grid.addWidget(Input_Parameter_Label[i], i, 0)
            grid.addWidget(Input_Parameter[i], i, 1)
            Bar_Label = QtWidgets.QLabel('|')
            Bar_Label.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
            grid.addWidget(Bar_Label, i, 2)

        self.initialvol = QtWidgets.QDoubleSpinBox()
        self.initialvol.setMaximum(99)
        self.initialvol.setDecimals(4)
        self.initialvol.setSingleStep(0.0001)
        self.initialvol.setValue(0.5)
        self.initialvol.setStatusTip('输入波动率初值，一般情况下不用更改')
        self.initialvol.setFixedWidth(140)
        self.initialvol.setFont(QtGui.QFont(Font_Label, FontSize))
        grid.addWidget(self.initialvol, 0, 4)
        Label = QtWidgets.QLabel('波动率初值')
        Label.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
        grid.addWidget(Label, 0, 3)

        self.callput = QtWidgets.QComboBox()
        self.callput.addItems(['看涨', '看跌'])
        self.callput.setFont(QtGui.QFont(Font_Label, FontSize))
        grid.addWidget(self.callput, 2, 4)
        typeLabel = QtWidgets.QLabel('&o: 期权类型')
        typeLabel.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
        typeLabel.setBuddy(self.callput)
        grid.addWidget(typeLabel, 2, 3)

        self.maturityDate = QtWidgets.QDateEdit()
        Tdate = datetime.now() + timedelta(days=30)
        self.maturityDate.setDate(QtCore.QDate(Tdate.year, Tdate.month, Tdate.day))
        self.maturityDate.setStatusTip('按到期日计算隐含波动率')
        self.maturityDate.setFixedWidth(140)
        self.maturityDate.setFont(QtGui.QFont(Font_Label, FontSize))
        grid.addWidget(self.maturityDate, 3, 4)
        self.maturityDate.hide()
        self.maturity = QtWidgets.QSpinBox()
        self.maturity.setValue(30)
        self.maturity.setMaximum(999999)
        self.maturity.setStatusTip('按期限计算隐含波动率')
        self.maturity.setFixedWidth(140)
        self.maturity.setFont(QtGui.QFont(Font_Label, FontSize))
        grid.addWidget(self.maturity, 3, 4)
        self.maturityLabel = QtWidgets.QComboBox()
        self.maturityLabel.addItems(['期限（天）', '到期日'])
        self.maturityLabel.currentTextChanged.connect(self.maturityTypeChanged)
        self.maturityLabel.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
        grid.addWidget(self.maturityLabel, 3, 3)

        optpricetypeLabel = QtWidgets.QLabel('输入期权价格')
        optpricetypeLabel.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
        grid.addWidget(optpricetypeLabel, 4, 3, 1, 2)

        self.optpricetype = QtWidgets.QComboBox()
        self.optpricetype.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
        self.optpricetype.addItems(['绝对价格', '相对价格'])
        grid.addWidget(self.optpricetype, 5, 3)

        self.optprice = QtWidgets.QDoubleSpinBox()
        self.optprice.setFixedWidth(140)
        self.optprice.setDecimals(4)
        self.optprice.setSingleStep(0.0001)
        self.optprice.setMaximum(99999)
        self.optprice.setStatusTip('输入期权价格')
        self.optprice.setFont(QtGui.QFont(Font_Label, FontSize))
        grid.addWidget(self.optprice, 5, 4)

        Label = QtWidgets.QLabel(' ')
        Label.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
        grid.addWidget(Label, 6, 0, 1, 3)

        Label = QtWidgets.QLabel('BSM隐含波动率：')
        Label.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
        Label.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(Label, 7, 0, 1, 3)
        Label = QtWidgets.QLabel('BAW隐含波动率：')
        Label.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
        Label.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(Label, 8, 0, 1, 3)

        Calculate_Btn = QtWidgets.QPushButton('计算', self)
        Calculate_Btn.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
        Calculate_Btn.setStatusTip('计算隐含波动率')
        Calculate_Btn.clicked.connect(self.ImpVolCalculate)
        grid.addWidget(Calculate_Btn, 9, 0, 1, 3)

        Quit_Btn = QtWidgets.QPushButton('退出', self)
        Quit_Btn.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
        Quit_Btn.setStatusTip('退出隐含波动率计算器')
        Quit_Btn.clicked.connect(self.close)
        grid.addWidget(Quit_Btn, 9, 3, 1, 3)

        self.BSMImpliedVol_Label = QtWidgets.QLabel()
        self.BSMImpliedVol_Label.setFont(QtGui.QFont(Font_Label, FontSize))
        self.BSMImpliedVol_Label.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.BSMImpliedVol_Label, 7, 3, 1, 3)

        self.BAWImpliedVol_Label = QtWidgets.QLabel()
        self.BAWImpliedVol_Label.setFont(QtGui.QFont(Font_Label, FontSize))
        self.BAWImpliedVol_Label.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.BAWImpliedVol_Label, 8, 3, 1, 3)

        self.move(300, 300)
        self.setWindowTitle('隐含波动率计算器')

    def ImpVolCalculate(self):
        try:
            K = self.strike.value()
            F = self.price.value()
            sigmai = self.initialvol.value()
            r = self.rate.value()
            q = self.dividend.value()
            ty = self.ty.value()
            epsilon = self.epsilon.value()
            opt = self.optprice.value()

            if self.optpricetype.currentText() == '相对价格':
                opt = opt * F
            if self.maturityLabel.currentText() == '期限（天）':
                T = float(self.maturity.text()) / ty
            else:
                mature = str(
                    self.maturityDate.date().year()
                ) + '-' + str(
                    self.maturityDate.date().month()
                ) + '-' + str(
                    self.maturityDate.date().day()
                )
                T = (
                    datetime.strptime(mature, '%Y-%m-%d') - datetime.now() + timedelta(days=1)
                ).days / ty
            if self.callput.currentText() == '看涨':
                OptionType = 'call'
            elif self.callput.currentText() == '看跌':
                OptionType = 'put'
        except:
            self.StatusBar.showMessage('参数输入错误，请检查参数')

        # try:
        #     opt = float(self.optprice.text())
        # except:
        #     self.StatusBar.showMessage('请输入正确的期权价格')

        try:
            # BSMImpliedVol = round(BSMImpVol(K, F, sigmai, r, T, q, OptionType, opt), 4)
            # BAWImpliedVol = round(BAWImpVol(K, F, sigmai, r, T, q, OptionType, epsilon, opt), 4)
            self.IV = IVThread(K, F, sigmai, r, T, q, OptionType, epsilon, opt)
            self.IV.start()
            self.IV.trigger.connect(self.IVshow)
        except:
            pass

    def IVshow(self):
        self.BSMImpliedVol_Label.setText(str(self.IV.BSMImpliedVol))
        self.BAWImpliedVol_Label.setText(str(self.IV.BAWImpliedVol))

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        self.close()

    def maturityTypeChanged(self):
        if self.maturityLabel.currentText() == '期限（天）':
            self.maturity.show()
            self.maturityDate.hide()
        else:
            self.maturityDate.show()
            self.maturity.hide()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = ImpliedVolatilityWindow()
    main.show()
    sys.exit(app.exec_())