using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Demo_3_4_WpfControlLibrary
{
    /// <summary>
    /// UserControl1.xaml 的交互逻辑
    /// </summary>
    public partial class BarControl : UserControl
    {
        public BarControl()
        {
            InitializeComponent();
        }
        #region 绘制直方图
        /// <summary>
        /// X轴步长（两个顶点点X轴的距离）
        /// </summary>
        public int StepLength = 60;
        /// <summary>
        /// 顶点最多个数
        /// </summary>
        public int MaxCount = 8;//
        /// <summary>
        /// 最大量程
        /// </summary>
        public int MaxReg = 100;//‘
        /// <summary>
        /// 最小量程
        /// </summary>
        public int MinReg = 60;//
        //底部数字列表
        List<TextBlock> listBottom = new List<TextBlock>();
        //线条列表
        List<Line> listLines = new List<Line>();
        /// <summary>
        /// 画线
        /// </summary>
        /// <param name="Y2">线段终点Y轴坐标</param>
        public void DrawLine(double Y2)
        {
            //将值转换为图上坐标
            Y2 = grdMain.Height - (grdMain.Height / (MaxReg - MinReg)) * (Y2 - MinReg);
            //判断折线图顶点集合个数是否大于0
            if (listLines.Count > 0)
            {
                Line line = new Line();
                //设置线条颜色
                line.Stroke = new SolidColorBrush(Colors.Honeydew);
                //设置线条宽度
                line.StrokeThickness = 20;

                line.X1 = (listLines[listLines.Count - 1].X1 + StepLength);
                line.Y1 = grdMain.Height;
                line.X2 = line.X1;
                line.Y2 = Y2;
                //向折线图顶点集合添加新线段终点坐标
                listLines.Add(line);
                //将折线控件作为子控件添加到界面
                this.grdMain.Children.Add(line);
                //判断顶点集合个数是否超过最大个数
                if (MaxCount < listLines.Count)
                {
                    //将曲线及下方数字往左移动

                    //删除第一个点
                    this.grdMain.Children.Remove(listLines[0]);
                    listLines.Remove(listLines[0]);
                    int ForLen = (listLines.Count > listBottom.Count) ? listLines.Count : listBottom.Count;
                    //将点击数字往左移动一位
                    for (int i = 0; i < ForLen; i++)
                    {
                        if (i < listLines.Count)
                        {
                            //将顶点的X轴坐标减去步长
                            listLines[i].X1 = listLines[i].X1 - StepLength;
                            listLines[i].X2 = listLines[i].X2 - StepLength;
                        }
                        if (i < listBottom.Count)
                        {
                            listBottom[i].Text = (int.Parse(listBottom[i].Text) + 1).ToString();
                        }
                    }
                }
            }
            else
            {//第一次添加顶点
                Line line = new Line();
                //设置线条颜色
                line.Stroke = new SolidColorBrush(Colors.Honeydew);
                //设置线条宽度
                line.StrokeThickness = 20;

                line.X1 = StepLength;
                line.Y1 = grdMain.Height;
                line.X2 = line.X1;
                line.Y2 = Y2;

                //向折线图顶点集合添加新线段终点坐标
                listLines.Add(line);
                //将折线控件作为子控件添加到界面
                this.grdMain.Children.Add(line);
            }

        }
        /// <summary>
        /// 绘制背景
        /// </summary>
        public void DrawBackground()
        {
            //清空
            grdBackground.Children.Clear();
            listBottom.Clear();
            //==============绘制底部数字及绘制Y轴方向直线
            //计算顶点最大个数
            MaxCount = (int)(grdBackground.Width / StepLength);
            for (int i = 1; i <= MaxCount; i++)
            {
                //绘制Y轴直线
                Line line = new Line();
                //设置开始坐标及终点坐标
                line.X1 = StepLength * i;
                line.X2 = StepLength * i;
                line.Y1 = 0;
                line.Y2 = grdBackground.Height;

                Color color = new Color();
                color.R = 20;
                color.G = 80;
                color.B = 136;
                color.A = 100;
                //设置线条颜色
                line.Stroke = new SolidColorBrush(color);
                //设置线条宽度
                line.StrokeThickness = 2;

                //绘制下方数字
                TextBlock tb = new TextBlock();
                //设置字体颜色
                tb.Foreground = new SolidColorBrush(Colors.Red);
                //数字
                tb.Text = "" + i;
                //显示界面
                grdBackground.Children.Add(tb);
                grdBackground.Children.Add(line);
                //添加到全局变量
                listBottom.Add(tb);
                //设置坐标
                Canvas.SetBottom(tb, -20);
                Canvas.SetLeft(tb, StepLength * i);
            }

            //==============绘制左侧数字及绘制X轴方向直线（大概原理同上）
            for (int i = MinReg; i <= MaxReg; i++)
            {
                Line line = new Line();
                line.X1 = 0;
                line.X2 = grdBackground.Width;
                //grdMain.Height - (grdMain.Height / (MaxReg-MinReg)) * Y2
                line.Y1 = grdMain.Height - (grdMain.Height / (MaxReg - MinReg)) * (i - MinReg);
                line.Y2 = grdMain.Height - (grdMain.Height / (MaxReg - MinReg)) * (i - MinReg);
                Color color = new Color();
                color.R = 20;
                color.G = 80;
                color.B = 136;
                color.A = 100;
                line.Stroke = new SolidColorBrush(color);
                line.StrokeThickness = 2;

                TextBlock tb = new TextBlock();
                tb.Foreground = new SolidColorBrush(Colors.Red);
                tb.Text = "" + i;
                grdBackground.Children.Add(tb);
                grdBackground.Children.Add(line);
                //  listBottom.Add(tb);
                Canvas.SetTop(tb, grdMain.Height - (grdMain.Height / (MaxReg - MinReg)) * (i - MinReg));
                Canvas.SetLeft(tb, -20);
            }
        }
        /// <summary>
        /// 清空柱状
        /// </summary>
        public void ClearLines()
        {
            //清空柱状集合
            listLines.Clear();
            //清空界面
            this.grdMain.Children.Clear();
        }
        #endregion

        private void UserControl_Loaded_1(object sender, RoutedEventArgs e)
        {
            DrawBackground();
        }

    }
}
