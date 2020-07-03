<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="ListShow.aspx.cs" Inherits="Demo_6.ListShow"  ViewStateMode="Enabled"%>

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
    </style>
</head>
<body>
    <form id="form1" runat="server">
        <div class="main">
            <asp:GridView ID="gvwUsers" runat="server" AutoGenerateColumns="False" CellPadding="4"
                ForeColor="#333333" GridLines="None"  OnRowDeleting="gvwUsers_RowDeleting">
                <FooterStyle BackColor="#990000" Font-Bold="True" ForeColor="White" />
                <Columns>
                    <asp:BoundField DataField="time" HeaderText="时间" ReadOnly="True" HeaderStyle-Width="200px" ItemStyle-HorizontalAlign="Center" />
                    <asp:TemplateField HeaderText="温度" HeaderStyle-Width="200px" ItemStyle-HorizontalAlign="Center">
                        <ItemTemplate>
                            <%#Eval("temp") %>
                        </ItemTemplate>
                        <EditItemTemplate>
                            <asp:TextBox ID="txtUserName" Text='<%# Eval("temp")%>' runat="server"></asp:TextBox>
                        </EditItemTemplate>
                    </asp:TemplateField>
                    <asp:TemplateField HeaderText="湿度" HeaderStyle-Width="200px" ItemStyle-HorizontalAlign="Center">
                        <ItemTemplate>
                            <%#Eval("hum") %>
                        </ItemTemplate>
                        <EditItemTemplate>
                            <asp:TextBox ID="txtUserPwd" Text='<%# Eval("hum")%>' runat="server"></asp:TextBox>
                        </EditItemTemplate>
                    </asp:TemplateField>
                    
                    <asp:CommandField HeaderText="删除" ShowDeleteButton="True" HeaderStyle-Width="100px" ItemStyle-HorizontalAlign="Center" />
                </Columns>
                <RowStyle ForeColor="#000066" />
                <SelectedRowStyle BackColor="#669999" Font-Bold="True" ForeColor="White" />
                <PagerStyle BackColor="White" ForeColor="#000066" HorizontalAlign="Left" />
                <HeaderStyle BackColor="#006699" Font-Bold="True" ForeColor="White" />
            </asp:GridView>
        </div>
    </form>
</body>
</html>
