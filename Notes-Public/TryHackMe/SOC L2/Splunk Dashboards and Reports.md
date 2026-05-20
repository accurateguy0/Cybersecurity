Until now, we have been using Splunk for broad searches mainly. However, we often need to run specific searches from time to time. For example, a certain organization might want to run a search every 8 hours when a new shift of SOC analysts arrives or is leaving. For this purpose, creating a report that will run at a specific time is efficient. Reports will then run the searches and save the results for viewing when the analysts for the incoming shift arrive.

Reports can also help reduce the load on the Splunk search head. For example, if multiple searches need to be run at the start of every shift, running them simultaneously can increase the search head's load and processing times. If searches are scheduled with 5 or 10-minute intervals, they will accomplish two tasks. 

1. The searches will run automatically without any user interaction.
2. The searches will not run simultaneously, reducing the possibility of errors or inefficiency.

Before moving forward, please start the attached VM by clicking the **Start Machine** button on the top right corner. Once the IP address is visible, you can use the URL: [http://10-65-159-230.reverse-proxy.cell-prod-us-east-1b.vm.tryhackme.com](http://10-65-159-230.reverse-proxy.cell-prod-us-east-1b.vm.tryhackme.com/) to access the Splunk instance. It might take 3-5 minutes for the Splunk instance to start. A VPN connection is not needed to access the Splunk instances.

Continuing from the previous task, move to the Reports tab to look at already saved reports in Splunk. We will see the following interface.

![A screenshot of the Reports tab in Splunk](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/0aed9fcd210b163c605284680efc430d.png)

Here, we see a list of reports already saved in Splunk. If we want to view the saved results of a report, we can click on the report's name. However, if we want to run a new search using the same query as the one in a report, we can use the 'Open in Search' option. The 'Edit' option allows us to edit the reports. The 'Next Scheduled Time' tab shows when the report will run again. We can also see the report's owner and its associated permissions. Please note that we have selected 'All' reports to be shown in the view above. There are options for viewing only the logged-in user's reports, as well as for viewing the reports added by the App. 

To create a new report, we can run a search and use the Save As option to save the search as a report.

![A screenshot of the 'Save As' option in the reports tab in Splunk](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/0cf70ab30e4b7e3ef7ee4909924bf7db.png)

Once we click the option to Save As Report, we see the following window.

![A screenshot focused on the Save As Report menu](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/7892bb7cb5332afca2520378eaee650b.png)

Filling in the required data and clicking the 'Save' option here will save the search as a report.

Let's practice the same in the attached Splunk instance. We ran a search in the previous task. To create a report on a search, we will first have to understand the data. On the left tab, we will see some fields Splunk has identified that might interest us. Let's click on hosts to see the number of hosts sending logs to our Splunk instance.

![A screenshot of logs in Splunk with the hosts field selected in the left tab](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/e7cd736aae3d8e8e234b8efea8cbf0d6.png)

So, we have 3 hosts; network-server, web-server, and vpn_server. They are all sending different numbers of events. If we are to determine the number of times each VPN user logged in during our given time window (which is 'all time' for this room), we will run the following query.

`host=vpn_server | stats count by Username`

This is what we get when we run this query in our instance.

![A screenshot of Splunk results showing usernames in descending order of number of occurrences as found in the results](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/a70e380a920c99fb120e94a15adefada.png)

In a SOC environment, we might want to track users who logged in during a certain time window. This requirement might be repetitive. SOC analysts can create a report for this requirement that will run every few hours for ease of use. Let's practice that based on what we learned in this task. First, we click 'Save As' and select 'Report'.

![A screenshot of Splunk focused on the Save As menu](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/a425a5b05047bcc8167e53f4f6233301.png)

We fill in the required information.

![A screenshot of Splunk Save As Report menu with details filled](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/a09eff4c9df3e76f6ddf989eba04e46d.png)

Here, we can see the Content for this report will be a 'Statistics Table' because we used 'stats count' in our query. The 'Time Range Picker' has been set to 'Yes'. This means running the report will give us a time-range picker option. When we click 'Save', we get the following prompt, telling us the report has been created.

![A screenshot of a message in Splunk informing the user that their report has been created](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/1e675560c1b6c0f2da5d65e15eacada4.png)

We can click the 'View' option to view our report. This is how it will look.

![A screenshot of a report as seen in Splunk](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/bafea3aec0dd48d8be76e2907c0d61c5.png)

On the reports tab, we can see our report now.

![A screenshot of the Reports menu in Splunk](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/2ea776d9ae008ead16058bb5d2f22ffe.png)

We see the owner of the report is 'admin', the logged-in user. The 'Sharing' is set to Private. This means that this report can only be accessed by admin. We can use the 'Edit' option to change the permissions and set it to be used by other users.

Splunk provides us with the ability to create dashboards and visualizations. These dashboards and visualizations provide a user with quick info about the data present in Splunk. Dashboards are often created to help give a brief overview of the most important bits of the data. They are often helpful in presenting data and statistics to the management, such as the number of incidents in a given time frame, or for SOC analysts to figure out where to focus, such as identifying spikes and drops in data sources, which might indicate a surge in, say, failed login attempts. The primary purpose of dashboards is to provide a quick visual overview of the available information. 

To move forward, let's create a dashboard in the attached VM. To start, move to the Dashboards tab. We will see the below screen.

![A screenshot of the Dashboards tab in Splunk highlighting the Create dashboards option, a list of dashboards, and properties of the created dashboards](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/7b578741a3241d45e848ddfac934e3af.png)

In this screen, we see an option to create dashboards labeled as 1 in the screenshot. Labeled as 2 is a list of available dashboards. Please note that we have selected 'All' dashboards here instead of 'Yours' or 'This App's', which can show a different list of dashboards. Labeled as 3 is information about these dashboards, such as owner, permissions, etc. Here, we also find the option to Edit the dashboard's different properties, or set it as the home dashboard. We can also view a dashboard by clicking on the name of the dashboard. However, we don't have any dashboards yet. We can start by creating a dashboard. For that, let's click the **Create Dashboard** option to see the following window.

![A screenshot of the Create New Dashboard option in Splunk](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/be9345e83d098e24621dc980759e89c0.png)

After filling in the relevant details, such as the name and permissions, we can choose one of the two options for dashboard creation through Classic Dashboards or Dashboard Studio. 

![A screenshot of the Create New Dashboard menu of Splunk with the details filled in](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/ae3bf1188ee513d8a5327da9d15d9932.png)

We can see that we have set the permissions to 'Shared in App'. This will ensure that the dashboard is also visible to other users of Splunk. We will use the Classic Dashboard approach to create a dashboard for this room. Let's do that and click 'Create'. The Window tells us to 'Click Add Panel to Start'. When we click the 'Add Panel' option, we get the following menu on the right side.

![A screenshot showing a blank, newly created dashboard in Splunk](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/1355c37ca97acafb650d7e30772624c8.png)

We want to add the results from our report to the Dashboard. We can select the 'New from Report' option to do that. 

![A screenshot focusing on the Add Panel option in the Dashboard edit menu in Splunk](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/8494ef44f7c6e667640b50cdc3c2e3e7.png)

The 'Add to Dashboard' option will add these results to our dashboard. However, we were already seeing the results as a report. What benefit will a dashboard provide us? The answer to that lies in visualizations. We can select a visualization from the menu, as shown below.

![A screenshot of a Splunk dashboard with the results of a report showing. The visualization option is highlighted which is showing a menu of charts to select from](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/6fd6d786cd7de2807bf0c7b61a782355.png)

Let's select the column chart visualization and check out the results.

![A screenshot of a splunk dashboard with the column chart visualization applied](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/0d4636314e99375e15ff798c886fc460.png)

Doesn't it look nice? We can see on a cursory glance that Emma logged in the least amount of times, and Sarah logged in the most. This is the kind of information that a dashboard is helpful for. Another way dashboards can help is by adding multiple reports to a single dashboard. The process for that will be similar, as we still see the Add Panel option above. However, we will keep this task to a single report. We can flip the switch to the Dark theme and click 'Save' to save the dashboard if we like it. This is how it will look when finished.

![A screenshot of a splunk dashboard with the column chart visualization and dark theme enabled](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/bdd06894dddfa316d0ec267df5f53e00.png)

Now, we can go to the Dashboards menu to see our newly created dashboard.

In the previous tasks, we practiced creating reports and dashboards. We understood that when we need to run a search repetitively, we can use reports, and if we want to club a few reports together or make visualizations, we can use dashboards. However, reports and dashboards will only be viewed by users at set time intervals. Sometimes, we want to be alerted if a certain event happens, such as, if the amount of failed logins on a single account reaches a threshold, it indicates a brute force attempt, and we would like to know as soon as it happens. In this task, we will learn how to set up alerts. Unfortunately, we cannot practice setting up alerts on the attached instance because of licensing issues. However, we will explain how to set up an alert in this task.

First, we will run a search for our required search term. In the 'Save As' drop-down, we will see an option for saving as an alert. In the previous task, we identified that the user Sarah logged in the most during our time range. Therefore, let's narrow down our search to all the login events of the user Sarah.

![A screenshot of Splunk results with the Save As option selected, showing an option to save the results as an alert](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/b62596f1ec7d35d8be5f5c060367f7b7.png)

When we click 'Alert' in the 'Save As' menu, we are asked to configure the alert's parameters.

![A screenshot of the Save As Alert menu in Splunk](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/75ef52a3c3b0a42d86fe76a3f52e1a7d.png)

We see the usual settings such as Title, Description and Permissions. In addition to that, we have some more options specific to alerts. The alert type we are setting up is scheduled. This means that Splunk will run this search as per the schedule, and if the trigger condition is satisfied, an alert will be raised. Depending on the license and configuration for your Splunk instance, you might get an option for scheduling Real-time alerts. Next, we have trigger conditions.

![Another screenshot of the Save As Alert menu, this time showing options not visible in the first screen shot](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/f0d21b2e8e03df5c9f3484e4087ff656.png)

Trigger conditions define the conditions when the alert will be raised. Here, let's say we raise the alert when the login count of our user is more than 5. In that case, we will use the 'Number of Results' option and set the 'is greater than' option to 5. We can trigger 5 alerts for the 5 login times, or we can just trigger a single alert for exceeding this count. The 'Throttle' option lets us limit the alerts by not raising an alert in the specified time period if an alert is already triggered. This can help reduce alert fatigue, which can overwhelm analysts when there are too many alerts. The final option here is for Trigger Actions. This option allows us to define what automated steps Splunk must take when the alert is triggered. For example, we might want Splunk to send an email to the SOC email account in case of an alert.

![A screenshot of trigger actions in the Save As Alert menu in Splunk](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/8a156dc2d6c94df4ae65aa458742c320.png)

Below, we can see the configured alert. We have configured it to run every hour if Sarah logs in more than 5 times. The email will only be sent once every 60 minutes.

![A screenshot of the Save As Alert menu with the details filled in](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/9960a9f78306e77c708469cf9f4ff582.png)

If the alert is triggered, Splunk will send an email to soc@tryhackme.com.

![Another screenshot of the Save As Alert menu with the details filled in, focusing on the trigger action of sending email](https://tryhackme-images.s3.amazonaws.com/user-uploads/61306d87a330ed00419e22e7/room-content/06eb3fdc2a3418db77adeb3bd1ec395a.png)

The email will be sent with the highest priority, and it will include the Subject and message mentioned above.