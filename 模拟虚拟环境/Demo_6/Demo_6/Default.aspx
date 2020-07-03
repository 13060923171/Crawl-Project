<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Default.aspx.cs" Inherits="Demo_6.Default" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title></title>
    <style>
        .main {
            width: 800px;
            height: 432px;
            background: url(Images/bg_main_menu.png);
        }

        image {
            width: 100%;
            height: 100%;
        }

        #btnLogin {
            background: #F0A401;
            width: 150px;
            height: 40px;
        }

        #btnResiger {
            width: 150px;
            height: 40px;
        }

        .tdl {
            font-size: 15pt;
            font-family: 'Microsoft YaHei UI';
        }

        .txt {
            width: 300px;
            height: 40px;
            font-size: 15pt;
        }
    </style>
</head>
<body>
    <form id="form1" runat="server">
        <div class="main">
            <table align="center">
                <tr>
                    <td colspan="2" style="text-align: center" class="tdl">监控登录</td>
                </tr>
                <tr>
                    <td class="tdl">用户名：</td>
                    <td>
                        <asp:TextBox ID="txtUserName" runat="server" CssClass="txt"></asp:TextBox></td>
                </tr>
                <tr>
                    <td class="tdl">密码：</td>
                    <td>
                        <input id="txtpwd" type="password" runat="server" class="txt" /></td>
                </tr>
                <tr>
                    <td colspan="2" style="text-align: center">
                        <asp:Button ID="btnLogin" runat="server" Text="登录" OnClick="btnLogin_Click" CssClass="tdl" />&nbsp;<asp:Button ID="btnResiger" runat="server" Text="注册" OnClick="btnResiger_Click" CssClass="tdl" /></td>
                </tr>
            </table>
        </div>
    </form>
</body>
</html>
