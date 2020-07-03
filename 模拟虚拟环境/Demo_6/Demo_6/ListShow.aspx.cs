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
    public partial class ListShow : System.Web.UI.Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack)
            {
                dataBinds();
            }
        }
        string sqlWhere = string.Empty;
        //绑定
        public void dataBinds()
        {
            string sql = "select * from TempHumData ";

            DataSet ds = SimpleSqlserverHelper.ExecuteDataset(sql);
            if (ds != null)
            {
                gvwUsers.DataSource = ds.Tables[0];
                gvwUsers.DataKeyNames = new string[] { "Id" };//主键
                gvwUsers.DataBind();
            }
        }

        /// <summary>
        /// 取消
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        //protected void gvwUsers_RowCancelingEdit(object sender, GridViewCancelEditEventArgs e)
        //{
        //    gvwUsers.EditIndex = -1;
        //    dataBinds();
        //}

        /// <summary>
        ///删除
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void gvwUsers_RowDeleting(object sender, GridViewDeleteEventArgs e)
        {
            sqlWhere = "delete from TempHumData  where Id='" + gvwUsers.DataKeys[e.RowIndex].Value.ToString() + "'";
            SimpleSqlserverHelper.ExecuteNonQuery(sqlWhere);
            dataBinds();
        }

        /// <summary>
        /// 编辑
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        //protected void gvwUsers_RowEditing(object sender, GridViewEditEventArgs e)
        //{
        //    gvwUsers.EditIndex = e.NewEditIndex;
        //    dataBinds();
        //}

        /// <summary>
        /// 更新
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        //protected void gvwUsers_RowUpdating(object sender, GridViewUpdateEventArgs e)
        //{
        //    string userName = ((TextBox)(gvwUsers.Rows[e.RowIndex].FindControl("txtUserName"))).Text.ToString().Trim();
        //    string userPwd = ((TextBox)(gvwUsers.Rows[e.RowIndex].FindControl("txtUserPwd"))).Text.ToString().Trim();

        //    string id = gvwUsers.DataKeys[e.RowIndex].Value.ToString();

        //    sqlWhere = "update Users set UserName='"
        //       + userName + "',UserPwd='"
        //       + userPwd + "' where UserId='"
        //      + id + "'";

        //    SimpleSqlserverHelper.ExecuteNonQuery(sqlWhere);

        //    gvwUsers.EditIndex = -1;
        //    dataBinds();
        //}



    }
}