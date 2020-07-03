using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
using System.Data.SqlClient;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Demo_6
{
    /// <summary>
    /// 简单SqlServer帮助类
    /// </summary>
    public static class SimpleSqlserverHelper
    {
        private static string ConnString;

        /// <summary>
        /// 读取配置
        /// </summary>
        /// <param name="key">配置名称（标识Key）</param>
        /// <returns></returns>
        public static string GetConfigValue(string key)
        {
            //若读取的Key不为null
            if (ConfigurationManager.AppSettings[key] != null)
            {
                //将读取到的值转换成
                return ConfigurationManager.AppSettings[key].ToString();
            }
            return string.Empty;
        }

        /// <summary>
        /// 静态构造函数
        /// </summary>
        static SimpleSqlserverHelper()
        {
            //取app.config的配置
            ConnString = GetConfigValue("ConnString");
        }

        /// <summary>
        /// ExecuteNonQuery
        /// </summary>
        /// <param name="commandText">SQL语句</param>
        /// <param name="commandParameters">参数</param>
        /// <returns></returns>
        public static int ExecuteNonQuery(string commandText, params SqlParameter[] commandParameters)
        {
            using (SqlConnection conn = new SqlConnection(ConnString))
            {
                conn.Open();
                SqlCommand cmd = new SqlCommand();
                cmd.Connection = conn;
                cmd.CommandText = commandText;
                foreach (SqlParameter para in commandParameters)
                {
                    cmd.Parameters.Add(para);
                }

                int ExeID = (int)(cmd.ExecuteNonQuery());
                conn.Close();
                return ExeID;
            }
        }

        /// <summary>
        /// ExecuteNonQuery
        /// </summary>
        /// <param name="commandText"></param>
        /// <returns></returns>
        public static int ExecuteNonQuery(string commandText)
        {
            using (SqlConnection conn = new SqlConnection(ConnString))
            {
                conn.Open();
                SqlCommand cmd = new SqlCommand();
                cmd.Connection = conn;
                cmd.CommandText = commandText;

                int ExeID = (int)(cmd.ExecuteNonQuery());
                conn.Close();
                return ExeID;
            }
        }

        public static DataSet ExecuteDataset(string commandText)
        {
            using (SqlConnection conn = new SqlConnection(ConnString))
            {
                conn.Open();
                SqlCommand cmd = new SqlCommand();
                cmd.Connection = conn;
                cmd.CommandText = commandText;

                using (SqlDataAdapter adapter = new SqlDataAdapter(cmd))
                {
                    adapter.SelectCommand = cmd;
                    DataSet dataSet = new DataSet();
                    adapter.Fill(dataSet);
                    cmd.Parameters.Clear();
                    return dataSet;
                };
            };
        }
        /// <summary>
        /// ExecuteDataset
        /// </summary>
        /// <param name="commandText"></param>
        /// <param name="commandParameters"></param>
        /// <returns></returns>
        public static DataSet ExecuteDataset(string commandText, params SqlParameter[] commandParameters)
        {
            using (SqlConnection conn = new SqlConnection(ConnString))
            {
                conn.Open();
                SqlCommand cmd = new SqlCommand();
                cmd.Connection = conn;
                cmd.CommandText = commandText;
                foreach (SqlParameter para in commandParameters)
                {
                    cmd.Parameters.Add(para);
                }
                using (SqlDataAdapter adapter = new SqlDataAdapter(cmd))
                {
                    adapter.SelectCommand = cmd;
                    DataSet dataSet = new DataSet();
                    adapter.Fill(dataSet);
                    cmd.Parameters.Clear();
                    return dataSet;
                };
            };
        }


        /// <summary>
        /// ExecuteReader
        /// </summary>
        /// <param name="strSql">SQL语句</param>
        /// <param name="Paras">参数</param>
        /// <returns></returns>
        public static SqlDataReader ExecuteReader(string commandText, params SqlParameter[] commandParameters)
        {
            using (SqlConnection conn = new SqlConnection(ConnString))
            {
                conn.Open();
                SqlCommand cmd = new SqlCommand();
                cmd.Connection = conn;
                cmd.CommandText = commandText;
                cmd.Parameters.AddRange(commandParameters);
                SqlDataReader sdr = cmd.ExecuteReader();
                return sdr;
            }
        }
    }
}
