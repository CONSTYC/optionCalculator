from PyQt5 import QtWidgets, QtGui, QtCore
from bin.PricingF import *
import sys

'''
Author : CCCCC
'''


class OptionCalculatorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(OptionCalculatorWindow, self).__init__()

        self.call = OptionProperty()
        self.put = OptionProperty()
        self.Call = OptionProperty()
        self.Put = OptionProperty()
        self.initUI()

    def initUI(self):
        FontSize = 10
        Font_Label = '微软雅黑'

        self.StatusBar = self.statusBar()

        grid = QtWidgets.QGridLayout()
        Vanilla_Center = QtWidgets.QWidget()
        Vanilla_Center.setLayout(grid)
        self.setCentralWidget(Vanilla_Center)

        Input_Parameter_Text = [
            '行权价', '市价', '波动率', '利率',
            '年天数', '期限（天）', '股息率', 'BAW精度'
        ]
        self.strike = QtWidgets.QDoubleSpinBox()
        self.strike.setDecimals(2)
        self.strike.setMaximum(999999.99)
        self.strike.setSingleStep(0.01)
        self.strike.setValue(100)
        self.strike.setStatusTip('输入行权价格')

        self.price = QtWidgets.QDoubleSpinBox()
        self.price.setDecimals(2)
        self.price.setMaximum(999999.99)
        self.price.setSingleStep(0.01)
        self.price.setValue(100)
        self.price.setStatusTip('输入当前市价')

        self.vol = QtWidgets.QDoubleSpinBox()
        self.vol.setDecimals(4)
        self.vol.setSingleStep(0.0001)
        self.vol.setValue(0.2)
        self.vol.setStatusTip('输入波动率')

        self.rate = QtWidgets.QDoubleSpinBox()
        self.rate.setDecimals(4)
        self.rate.setSingleStep(0.0001)
        self.rate.setValue(0.03)
        self.rate.setStatusTip('输入无风险利率')

        self.ty = QtWidgets.QSpinBox()
        self.ty.setMaximum(366)
        self.ty.setValue(360)
        self.ty.setStatusTip('输入一年的天数')

        self.maturity = QtWidgets.QSpinBox()
        self.maturity.setMaximum(999999)
        self.maturity.setValue(30)
        self.maturity.setStatusTip('输入期权期限')

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
            self.strike, self.price, self.vol, self.rate,
            self.ty, self.maturity, self.dividend, self.epsilon
        ]
        strikeLabel = QtWidgets.QLabel('&K: ' + Input_Parameter_Text[0])
        priceLabel = QtWidgets.QLabel('&F: ' + Input_Parameter_Text[1])
        volLabel = QtWidgets.QLabel('&V: ' + Input_Parameter_Text[2])
        rateLabel = QtWidgets.QLabel('&r: ' + Input_Parameter_Text[3])
        tyLabel = QtWidgets.QLabel('&y: ' + Input_Parameter_Text[4])
        maturityLabel = QtWidgets.QLabel('&T: ' + Input_Parameter_Text[5])
        dividendLabel = QtWidgets.QLabel('&q: ' + Input_Parameter_Text[6])
        epsilonLabel = QtWidgets.QLabel('&e: ' + Input_Parameter_Text[7])
        Input_Parameter_Label = [
            strikeLabel, priceLabel, volLabel, rateLabel, tyLabel,
            maturityLabel, dividendLabel, epsilonLabel
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
            grid.addWidget(Bar_Label, i, 2)

        European_Label = QtWidgets.QLabel('欧式')
        European_Label.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
        grid.addWidget(European_Label, 0, 3)
        American_Label = QtWidgets.QLabel('美式')
        American_Label.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
        grid.addWidget(American_Label, 0, 7)

        self.BSMc_Text = QtWidgets.QLabel(self.call.Value)
        self.BSMp_Text = QtWidgets.QLabel(self.put.Value)
        self.BAWC_Text = QtWidgets.QLabel(self.Call.Value)
        self.BAWP_Text = QtWidgets.QLabel(self.Put.Value)

        self.BSMcDelta_Text = QtWidgets.QLabel(self.call.Delta)
        self.BSMcGamma_Text = QtWidgets.QLabel(self.call.Gamma)
        self.BSMcVega_Text = QtWidgets.QLabel(self.call.Vega)
        self.BSMcTheta_Text = QtWidgets.QLabel(self.call.Theta)

        self.BSMpDelta_Text = QtWidgets.QLabel(self.put.Delta)
        self.BSMpGamma_Text = QtWidgets.QLabel(self.put.Gamma)
        self.BSMpVega_Text = QtWidgets.QLabel(self.put.Vega)
        self.BSMpTheta_Text = QtWidgets.QLabel(self.put.Theta)

        self.BAWCDelta_Text = QtWidgets.QLabel(self.Call.Delta)
        self.BAWCGamma_Text = QtWidgets.QLabel(self.Call.Gamma)
        self.BAWCVega_Text = QtWidgets.QLabel(self.Call.Vega)
        self.BAWCTheta_Text = QtWidgets.QLabel(self.Call.Theta)

        self.BAWPDelta_Text = QtWidgets.QLabel(self.Put.Delta)
        self.BAWPGamma_Text = QtWidgets.QLabel(self.Put.Gamma)
        self.BAWPVega_Text = QtWidgets.QLabel(self.Put.Vega)
        self.BAWPTheta_Text = QtWidgets.QLabel(self.Put.Theta)

        Option_Parameter_Name = ['BSM看涨', 'BSM看跌', 'BAW看涨', 'BAW看跌']
        Option_Widget = [
            self.BSMc_Text, self.BSMp_Text, self.BAWC_Text, self.BAWP_Text
        ]
        Greeks_Parameter_Name = ['Delta', 'Gamma', 'Vega', 'Theta']
        Greeks_Widget = [
            [self.BSMcDelta_Text, self.BSMcGamma_Text, self.BSMcVega_Text, self.BSMcTheta_Text],
            [self.BSMpDelta_Text, self.BSMpGamma_Text, self.BSMpVega_Text, self.BSMpTheta_Text],
            [self.BAWCDelta_Text, self.BAWCGamma_Text, self.BAWCVega_Text, self.BAWCTheta_Text],
            [self.BAWPDelta_Text, self.BAWPGamma_Text, self.BAWPVega_Text, self.BAWPTheta_Text]
        ]
        for i in range(len(Option_Parameter_Name)):
            Option_Label = QtWidgets.QLabel(Option_Parameter_Name[i])
            Option_Label.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
            grid.addWidget(Option_Label, 1, 3 + i * 2)
            Option_Label_Blank = QtWidgets.QLabel('                 ')
            Option_Label_Blank.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
            grid.addWidget(Option_Label_Blank, 1, 4 + i * 2)
            Option_Widget[i].setFont(QtGui.QFont(Font_Label, FontSize))
            Option_Widget[i].setAlignment(QtCore.Qt.AlignCenter)
            Option_Widget[i].setStatusTip('相对报价为：0.00%')
            grid.addWidget(Option_Widget[i], 1, 4 + i * 2)
            for j in range(len(Greeks_Parameter_Name)):
                Greeks_Label = QtWidgets.QLabel(Greeks_Parameter_Name[j])
                Greeks_Label.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
                grid.addWidget(Greeks_Label, j + 3, 3 + i * 2)
                Greeks_Widget[i][j].setFont(QtGui.QFont(Font_Label, FontSize))
                Greeks_Widget[i][j].setAlignment(QtCore.Qt.AlignCenter)
                grid.addWidget(Greeks_Widget[i][j], j + 3, 4 + i * 2)

        Calculate_Btn = QtWidgets.QPushButton('计算', self)
        Calculate_Btn.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
        Calculate_Btn.setStatusTip('计算')
        Calculate_Btn.clicked.connect(self.OptionCalculate)
        grid.addWidget(Calculate_Btn, 7, 3, 1, 4)

        Quit_Btn = QtWidgets.QPushButton('退出', self)
        Quit_Btn.setFont(QtGui.QFont(Font_Label, FontSize, QtGui.QFont.Bold))
        Quit_Btn.setStatusTip('退出期权计算器')
        Quit_Btn.clicked.connect(self.close)
        grid.addWidget(Quit_Btn, 7, 7, 1, 4)

        # self.setFixedSize()
        self.move(400, 400)
        self.setWindowTitle('香草期权计算器')
        # self.show()

    def OptionCalculate(self):
        try:
            K = self.strike.value()
            F = self.price.value()
            sigma = self.vol.value()
            r = self.rate.value()
            T = self.maturity.value() / self.ty.value()
            q = self.dividend.value()
            epsilon = self.epsilon.value()
            d = 0.001
            # BSM看涨
            self.call.Value = str(round(PricingBSM(K, F, sigma, r, T, q, 'call'), 4))
            self.BSMc_Text.setText(self.call.Value)
            self.BSMc_Text.setStatusTip(
                '相对报价为：' + str(
                    round(float(self.call.Value) / float(self.price.text()), 4) * 100
                ) + '%')

            self.call.Delta = str(round(BSMDelta(K, F, sigma, r, T, q, 'call'), 4))
            self.BSMcDelta_Text.setText(self.call.Delta)

            self.call.Gamma = str(round(BSMGamma(K, F, sigma, r, T, q), 4))
            self.BSMcGamma_Text.setText(self.call.Gamma)

            self.call.Vega = str(round(BSMVega(K, F, sigma, r, T, q), 4))
            self.BSMcVega_Text.setText(self.call.Vega)

            self.call.Theta = str(round(-BSMTheta(K, F, sigma, r, T, q, 'call'), 4))
            self.BSMcTheta_Text.setText(self.call.Theta)

            # BSM看跌
            self.put.Value = str(round(PricingBSM(K, F, sigma, r, T, q, 'put'), 4))
            self.BSMp_Text.setText(self.put.Value)
            self.BSMp_Text.setStatusTip(
                '相对报价为：' + str(
                    round(float(self.put.Value) / float(self.price.text()), 4) * 100
                ) + '%')

            self.put.Delta = str(round(BSMDelta(K, F, sigma, r, T, q, 'put'), 4))
            self.BSMpDelta_Text.setText(self.put.Delta)

            self.put.Gamma = str(round(BSMGamma(K, F, sigma, r, T, q), 4))
            self.BSMpGamma_Text.setText(self.put.Gamma)

            self.put.Vega = str(round(BSMVega(K, F, sigma, r, T, q), 4))
            self.BSMpVega_Text.setText(self.put.Vega)

            self.put.Theta = str(round(-BSMTheta(K, F, sigma, r, T, q, 'put'), 4))
            self.BSMpTheta_Text.setText(self.put.Theta)

            # BAW看涨
            self.Call.Value = str(round(PricingBAW(K, F, sigma, r, T, q, 'call', epsilon), 4))
            self.BAWC_Text.setText(self.Call.Value)
            self.BAWC_Text.setStatusTip(
                '相对报价为：' + str(
                    round(float(self.Call.Value) / float(self.price.text()), 4) * 100
                ) + '%')

            self.Call.Delta = str(round(
                (
                    PricingBAW(K, F * (1 + d), sigma, r, T, q, 'call', epsilon)
                    - PricingBAW(K, F * (1 - d), sigma, r, T, q, 'call', epsilon)
                ) / (2 * d * F), 4
            ))
            self.BAWCDelta_Text.setText(self.Call.Delta)

            self.Call.Gamma = str(round(
                (
                    PricingBAW(K, F * (1 + d), sigma, r, T, q, 'call', epsilon)
                    + PricingBAW(K, F * (1 - d), sigma, r, T, q, 'call', epsilon)
                    - 2 * PricingBAW(K, F, sigma, r, T, q, 'call', epsilon)
                ) / (d * F) ** 2, 4
            ))
            self.BAWCGamma_Text.setText(self.Call.Gamma)

            self.Call.Vega = str(round(
                (
                    PricingBAW(K, F, sigma * (1 + d), r, T, q, 'call', epsilon)
                    - PricingBAW(K, F, sigma * (1 - d), r, T, q, 'call', epsilon)
                ) / (2 * d * sigma), 4
            ))
            self.BAWCVega_Text.setText(self.Call.Vega)

            self.Call.Theta = str(round(
                (
                    PricingBAW(K, F, sigma, r, T * (1 + d), q, 'call', epsilon)
                    - PricingBAW(K, F, sigma, r, T * (1 - d), q, 'call', epsilon)
                ) / (2 * d * T), 4
            ))
            self.BAWCTheta_Text.setText(self.Call.Theta)

            # BAW看跌
            self.Put.Value = str(round(PricingBAW(K, F, sigma, r, T, q, 'put', epsilon), 4))
            self.BAWP_Text.setText(self.Put.Value)
            self.BAWP_Text.setStatusTip(
                '相对报价为：' + str(
                    round(float(self.Put.Value) / float(self.price.text()), 4) * 100
                ) + '%')

            self.Put.Delta = str(round(
                (
                    PricingBAW(K, F * (1 + d), sigma, r, T, q, 'put', epsilon)
                    - PricingBAW(K, F * (1 - d), sigma, r, T, q, 'put', epsilon)
                ) / (2 * d * F), 4
            ))
            self.BAWPDelta_Text.setText(self.Put.Delta)

            self.Put.Gamma = str(round(
                (
                    PricingBAW(K, F * (1 + d), sigma, r, T, q, 'put', epsilon)
                    + PricingBAW(K, F * (1 - d), sigma, r, T, q, 'put', epsilon)
                    - 2 * PricingBAW(K, F, sigma, r, T, q, 'put', epsilon)
                ) / (d * F) ** 2, 4
            ))
            self.BAWPGamma_Text.setText(self.Put.Gamma)

            self.Put.Vega = str(round(
                (
                    PricingBAW(K, F, sigma * (1 + d), r, T, q, 'put', epsilon)
                    - PricingBAW(K, F, sigma * (1 - d), r, T, q, 'put', epsilon)
                ) / (2 * d * sigma), 4
            ))
            self.BAWPVega_Text.setText(self.Put.Vega)

            self.Put.Theta = str(round(
                (
                    PricingBAW(K, F, sigma, r, T * (1 + d), q, 'put', epsilon)
                    - PricingBAW(K, F, sigma, r, T * (1 - d), q, 'put', epsilon)
                ) / (2 * d * T), 4
            ))
            self.BAWPTheta_Text.setText(self.Put.Theta)
            self.StatusBar.showMessage('计算完成')
        except:
            self.StatusBar.showMessage('参数输入错误，请检查参数')

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        self.close()


class OptionProperty(object):
    def __init__(self):
        self.Value = '0.0000'
        self.Delta = '0.0000'
        self.Vega = '0.0000'
        self.Theta = '0.0000'

        self.Gamma = '0.0000'
        self.Vanna = '0.0000'
        self.Vomma = '0.0000'
        self.Charm = '0.0000'
        self.Veta = '0.0000'

        self.Color = '0.0000'
        self.Speed = '0.0000'
        self.Zomma = '0.0000'


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = OptionCalculatorWindow()
    main.show()
    sys.exit(app.exec_())
