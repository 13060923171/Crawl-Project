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
using System.Windows.Shapes;

namespace WpfApp2
{
    /// <summary>
    /// Logit.xaml 的交互逻辑
    /// </summary>
    public partial class Logit : Window
    {
        /// <summary>
        /// MainWindow.xaml 的交互逻辑
        /// </summary>

        public Logit()
        {
            InitializeComponent();
        }

        //用户名
        private string UserName = "";
        //用户密码
        private string UserPwd = "";
        //用户性别
        private string UserGender = "";
        //用户籍贯
        private string UserOriginName = "";
        //用户爱好
        private string UserHobbies = "";
        //用户建议
        private string UserSuggest = "";
        #region Welcome

        private void grdWelcome_MouseDown_1(object sender, MouseButtonEventArgs e)
        {
            GridShow(grdLogin);
        }
        #endregion
        #region Registered

        private void btnRegisteredCancel_Click_1(object sender, RoutedEventArgs e)
        {
            GridShow(grdLogin);
            txtRegisteredUserName.Text = "";
            pwdRegisteredUserPwd1.Password = "";
            pwdRegisteredUserPwd2.Password = "";
        }

        private void btnRegistered_Click_1(object sender, RoutedEventArgs e)
        {
            //信息完整检测
            if (txtRegisteredUserName.Text == "" ||
                pwdRegisteredUserPwd1.Password.ToString() == "" ||
                pwdRegisteredUserPwd2.Password.ToString() == "")
            {
                MessageBox.Show("请填写完整！", "提示", MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            //两次密码一致性检测
            if (pwdRegisteredUserPwd1.Password.ToString() !=
                pwdRegisteredUserPwd2.Password.ToString())
            {
                MessageBox.Show("两次密码不一致,请重新输入！", "提示", MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            //注册成功===========================
            //用户名
            UserName = txtRegisteredUserName.Text;
            //密码
            UserPwd = pwdRegisteredUserPwd1.Password.ToString();
            //性别
            if (rbtnBoy.IsChecked != null)
            {
                UserGender = (((bool)rbtnBoy.IsChecked) ? "男" : "女");
            }
            else
            {
                UserGender = "女";
            }

            //爱好
            CheckBox[] HobbiesS = new CheckBox[] { chkSports, chkInternetChat, chkHobbiesOther };
            UserHobbies = "";
            for (int i = 0; i < HobbiesS.Length; i++)
            {
                CheckBox chk = HobbiesS[i];
                if (chk.IsChecked == true && chk.Content != "")
                {
                    UserHobbies += chk.Content.ToString();
                }
                else if (chk.IsChecked == true)
                {
                    UserHobbies += txtHobbiesOther.Text;
                }
            }
            //籍贯
            UserOriginName = "";
            if (cboOriginName.IsEnabled == true)
            {
                UserOriginName = cboOriginName.Text;
            }
            //建议
            UserSuggest = txtSuggest.Text;
            MessageBox.Show(
                "用户名：" + UserName + "\r\n" +
                "性　别：" + UserGender + "\r\n" +
                "籍　贯：" + UserOriginName + "\r\n" +
                "爱　好：" + UserHobbies + "\r\n" +
                "建　议：" + UserSuggest + "\r\n" +
                "注册成功！", "提示", MessageBoxButton.OK, MessageBoxImage.Information);

            GridShow(grdLogin);
            txtRegisteredUserName.Text = "";
            pwdRegisteredUserPwd1.Password = "";
            pwdRegisteredUserPwd2.Password = "";
        }
        /// <summary>
        /// 籍贯类型选择事件
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void cboOriginType_SelectionChanged_1(object sender, SelectionChangedEventArgs e)
        {
            string[] OriginTypeName = new string[0];
            switch (cboOriginType.SelectedIndex)
            {
                case 0:
                    {
                        //省
                        OriginTypeName = new string[]{
                            "河北省",
                            "山西省",
                            "辽宁省",
                            "吉林省",
                            "黑龙江省",
                            "江苏省",
                            "浙江省",
                            "安徽省",
                            "福建省",
                            "江西省",
                            "山东省",
                        "河南省",
                        "湖北省",
                        "湖南省",
                        "广东省",
                        "海南省",
                        "四川省",
                        "贵州省",
                        "云南省",
                        "陕西省",
                        "甘肃省",
                        "青海省",
                        "台湾省"

                       };
                    }
                    break;
                case 1:
                    {//直辖市
                        OriginTypeName = new string[] {
                        "北京",
                        "天津",
                        "上海",
                        "重庆"
                        };
                    }
                    break;
                case 2:
                    {
                        //自治区
                        OriginTypeName = new string[] {
                        "新疆维吾尔族自治区",
                        "广西壮族自治区",
                        "宁夏回族自治区",
                        "内蒙古自治区",
                        "西藏自治区"
                        };
                    }
                    break;
                default:
                    break;
            }
            if (OriginTypeName.Length > 0)
            {
                cboOriginName.ItemsSource = OriginTypeName;
                if (cboOriginName.IsEnabled == false)
                {
                    cboOriginName.IsEnabled = true;
                }
            }
            else
            {
                cboOriginName.IsEnabled = false;
            }
        }
        #endregion
        #region Login

        private void btnRegisteredShow_Click_1(object sender, RoutedEventArgs e)
        {
            GridShow(grdRegistered);
            txtLoginUserName.Text = "";
            pwdLoginUserPwd.Password = "";
        }

        private void btnLogin_Click_1(object sender, RoutedEventArgs e)
        {
            //不正确信息
            string Msg = "";
            //用户名检测
            if (txtLoginUserName.Text != UserName || txtLoginUserName.Text == "")
            {
                Msg = "用户名";
            }
            //密码检测
            if (pwdLoginUserPwd.Password.ToString() != UserPwd || pwdLoginUserPwd.Password.ToString() == "")
            {
                if (Msg != "")
                {
                    Msg += "、";
                }
                Msg += "密码";
            }
            //检测结果处理
            if (Msg != "")
            {
                Msg += "错误";
                if (UserPwd == "" && UserName == "")
                {//未注册
                    Msg += ",请进行注册操作！";
                }
                //错误提示
                MessageBox.Show(Msg, "错误", MessageBoxButton.OK, MessageBoxImage.Error);
            }
            else
            {//登陆成功
                GridShow(grdWelcome);
                txtLoginUserName.Text = "";
                pwdLoginUserPwd.Password = "";
            }
        }
        #endregion
        private void GridShow(Grid grd)
        {
            grdRegistered.Visibility = Visibility.Hidden;
            grdLogin.Visibility = Visibility.Hidden;
            grdWelcome.Visibility = Visibility.Hidden;
            grd.Visibility = Visibility.Visible;
        }

        private void Window_Loaded_1(object sender, RoutedEventArgs e)
        {
            GridShow(grdLogin);
        }



        private void Button_Click_1(object sender, RoutedEventArgs e)
        {
            MainWindow mw = new MainWindow();

            mw.Show();

            this.Hide();//当前窗体隐藏
        }
    }

}

