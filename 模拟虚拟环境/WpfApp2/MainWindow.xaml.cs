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

using System.IO.Ports;
using Modbus.Device;
using System.Threading;
using System.Data.SqlClient;


namespace WpfApp2
{
    /// <summary>
    /// MainWindow.xaml 的交互逻辑
    /// </summary>
    public partial class MainWindow : Window
    {

        //存储温湿度数据

        int num = 0;
        double temp = 0;
        double hum = 0;
        
        //实例化IModbusMaster 对象master
        private static IModbusMaster master;
        //使用串行端口资源SerialPort对象com
        SerialPort com = new SerialPort();
        //写寄存器数组
        private ushort[] registerBuffer;
        public MainWindow()
        {
            InitializeComponent();
            //添加窗体加载事件
            this.Loaded += MainWindow_Loaded;
        }

        Thread timer;//声明线程变量

        void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            //获取本机所有串口的名字
            string[] strPortName = SerialPort.GetPortNames();
            //将本机所有串口名称复制给cmbPort控件
            cmbPort.ItemsSource = strPortName;

            //下拉框初始化
            //如果本机串口数量不为0，则将cmbPort设为Item的第一个索引
            if (strPortName.Length > 0) cmbPort.SelectedIndex = 0;
            //将波特率下拉框cmbBaudRate的设为Item的第一个索引
            cmbBaudRate.SelectedIndex = 0;
            //将数据位下拉框cmbBaudRate的设为Item的第一个索引
            cmbDataBits.SelectedIndex = 0;
            //将停止位下拉框cmbBaudRate的设为Item的第一个索引
            cmbStopBits.SelectedIndex = 0;
            //将奇偶校验位下拉框cmbBaudRate的设为Item的第一个索引
            cmbParity.SelectedIndex = 0;

            //绘制背景
            CurveCtr.DrawBackground();
            BarCtr.DrawBackground();
            timer = new Thread(new ThreadStart(() =>//线程实例化
            {
                while (true)
                {
                    try
                    {
                        Dispatcher.Invoke(new Action(() =>
                        {
                            CurveCtr.DrawLine(temp);//绘制温度折线
                            BarCtr.DrawLine(hum);//绘制湿度直方图
                        }));
                    }
                    catch (Exception)
                    {
                    }
                    Thread.Sleep(700);
                }
            }));
            timer.Start();//开启线程
        }

        private void Window_Closing_1(object sender, System.ComponentModel.CancelEventArgs e)
        {
            timer.Abort();//关闭线程
            timer = null;
        }

        private void btnOpen_Click(object sender, RoutedEventArgs e)
        {
            //如果按钮内容是“打开串口”则进行打开串口，否则关闭串口
            if (btnOpen.Content.ToString() == "打开串口")
            {
                //尝试执行打开串口，出错则在界面出现提示
                try
                {
                    //判断串口是否已经打开
                    if (!com.IsOpen)
                    {
                        //设置串口参数******************************************开始
                        com.PortName = cmbPort.Text;//串口号
                        com.BaudRate = int.Parse(cmbBaudRate.Text);//波特率
                        com.DataBits = int.Parse(cmbDataBits.Text);//数据位
                        switch (cmbStopBits.SelectedIndex)//停止位
                        {
                            case 0:
                                com.StopBits = StopBits.One; break;
                            case 1:
                                com.StopBits = StopBits.Two; break;
                            case 2:
                                com.StopBits = StopBits.OnePointFive; break;
                            case 3:
                                com.StopBits = StopBits.None; break;
                        }
                        switch (cmbParity.SelectedIndex)//奇偶校验
                        {
                            case 0:
                                com.Parity = Parity.None; break;
                            case 1:
                                com.Parity = Parity.Odd; break;
                            case 2:
                                com.Parity = Parity.Even; break;

                        }
                        //设置串口参数******************************************结束
                        master = ModbusSerialMaster.CreateRtu(com);
                        com.Open();//打开串口

                    }
                    //设置按钮内容为关闭串口
                    btnOpen.Content = "关闭串口";
                    //界面显示信息“串口已打开”
                    txtStatus.Text = "串口已打开！\n";
                }
                catch
                {
                    txtStatus.Text = "串口已打开错误或串口不存在！！";
                }
            }
            else//关闭串口
            {
                try
                {
                    if (com.IsOpen)
                        com.Close();//关闭串口
                    btnOpen.Content = "打开串口";
                    txtStatus.Text = "串口已关闭！";

                }
                catch
                {
                    txtStatus.Text = "串口已打开错误或串口不存在！！";
                }
            }
        }

        private void BtnReceive_Click(object sender, RoutedEventArgs e)
        {
            txtStatus.Clear();

            if (com.IsOpen == false)
            {
                txtStatus.AppendText("请打开串口！！\r\n");

            }
            else
            {
                //读取温度便送器寄存器中的数据
                registerBuffer = master.ReadHoldingRegisters(1, 0, 2);
                temp = registerBuffer[0] / 1.0;
                txtStatus.AppendText("温度：" + temp + "°C" + "\n");
                hum = registerBuffer[1] / 1.0;
                txtStatus.AppendText("湿度：" + hum + "%" + "\r\n");
            }
        }

        private void Btn_salve_Click(object sender, RoutedEventArgs e)
        {
            //创建数据库连接
            //声明数据库连接变量
            //Data Source=(localdb)\MSSQLLocalDB;Initial Catalog=logit;Integrated Security=True;Pooling=False
            string connString = @"Data Source=(localdb)\MSSQLLocalDB;Initial Catalog=Users;Integrated Security=True;Pooling=False";
            //数据库查值调用
            try
            {
                using (SqlConnection conn = new SqlConnection(connString))
                {
                    conn.Open();//打开数据库
                    string sqlSel = String.Format("SELECT MAX(Id) FROM TempHumData");
                    SqlCommand commSel = new SqlCommand(sqlSel, conn);//创建Command对象
                    if (!(commSel.ExecuteScalar() == null))
                    {
                        num = (int)commSel.ExecuteScalar();
                        num++;
                    }
                    string sqlIns = String.Format("INSERT INTO TempHumData(Id,time,temp,hum) " +
               "VALUES('{0}','{1}','{2}','{3}')", num, DateTime.Now, temp, hum);
                    SqlCommand commIns = new SqlCommand(sqlIns, conn);//创建Command对象
                    int n = commIns.ExecuteNonQuery();//执行添加命令，返回值为更新的行数
                    if (n > 0)
                    {
                        txtStatus.AppendText("数据保存成功！！！！" + "\r\n");
                    }

                    else
                    {
                        txtStatus.AppendText("数据保存失败！！！！" + "\r\n");
                    }

                }
            }
            catch (Exception ex)
            {

                txtStatus.AppendText(ex.Message + "\r\n");
            }


        }
    

    }
}
