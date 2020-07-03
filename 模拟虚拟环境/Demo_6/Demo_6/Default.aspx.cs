using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Demo_6
{
    public partial class Default : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {

        }

        /// <summary>
        /// 登录
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void btnLogin_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtUserName.Text))
            {
                Response.Write("<script>alert('请输入用户名')</script>");
                return;
            }
            if (string.IsNullOrWhiteSpace(txtpwd.Value))
            {
                Response.Write("<script>alert('请输入密码')</script>");
                return;
            }

            //sql查询语句
            string sql = "select UserId from Users where UserName=@username and UserPwd=@userpwd";
            //设置参数
            SqlParameter[] paras = new SqlParameter[]
                {
                    //记录数据ID
                    new SqlParameter("@username", SqlDbType.NVarChar,50),
                     new SqlParameter("@userpwd", SqlDbType.NVarChar,50)
                };

            paras[0].Value = txtUserName.Text;
            paras[1].Value = txtpwd.Value;

            DataSet ds = SimpleSqlserverHelper.ExecuteDataset(sql, paras);

            if (ds != null && ds.Tables[0] != null && ds.Tables[0].Rows.Count > 0)
            {
                Response.Write("<script>alert('登录成功')</script>");
                Response.Redirect("ListShow.aspx");
            }
            else
            {
                Response.Write("<script>alert('登录失败')</script>");
            }

        }

        /// <summary>
        /// 注册
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void btnResiger_Click(object sender, EventArgs e)
        {
            Response.Redirect("Resiger.aspx");
        }
    }
}