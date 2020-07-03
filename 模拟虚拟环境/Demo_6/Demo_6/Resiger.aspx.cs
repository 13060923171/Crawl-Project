using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Demo_6
{
    public partial class Resiger : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {

        }

        /// <summary>
        /// 注册
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void btnRegister_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtUserName.Text))
            {
                Response.Write("<script>alert('请输入用户名')</script>");
                return;
            }
            if (string.IsNullOrWhiteSpace(txtUserPwd.Value))
            {
                Response.Write("<script>alert('请输入密码')</script>");
                return;
            }

            int id = SimpleSqlserverHelper.ExecuteNonQuery("Insert into Users (UserName,UserPwd)Values('" + txtUserName.Text + "','" + txtUserPwd.Value + "')");

            if (id > 0)
            {
                Response.Write("<script>alert('注册成功')</script>");
                Response.Redirect("Default.aspx");
            }
            else
            {
                Response.Write("<script>alert('注册失败')</script>");
            }
        }
    }
}