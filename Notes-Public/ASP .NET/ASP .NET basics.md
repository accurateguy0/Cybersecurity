If you want to prevent your content blocks or layout files from being viewed by your users, rename the files to:

\_header.cshtml

\_footer.cshtml

\_Layout.cshtml
## Hiding Sensitive Information

With ASP.NET, the common way to hide sensitive information (database passwords, email passwords, etc.) is to keep the information in a separate file named "_AppStart".

### _AppStart.cshtml

@{  
WebMail.SmtpServer = "mailserver.example.com";  
WebMail.EnableSsl = true;  
WebMail.UserName = "username@example.com";  
WebMail.Password = "your-password";  
WebMail.From = "your-name-here@example.com";  
}

dotnet new list - presents the list of templates
