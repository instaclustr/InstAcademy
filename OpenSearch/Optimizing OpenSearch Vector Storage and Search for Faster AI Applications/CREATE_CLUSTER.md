# Creating a NetApp Instaclustr Cluster

**Vector Storage & Search for AI** · [← Course index](README.md) · [← How to run labs](HANDS-ON-GUIDE.md)

First, you'll want to start the sign-up process at (attribution link).

## Sign up

After filling out the form:

![](./img/signup.png)

You'll be taken to the dashboard, where you'll be asked to verify your email address:

![](./img/verify_email.png)

Once you've done so, the yellow dialog box will disappear:

![](./img/email_verified.png)

and you'll be ready to create your cluster.

## Create cluster

First, on the dashboard, select the blue 'Create Cluster' button in the left sidebar:

![](./img/create_cluster.png)

Give your cluster a name and select 'OpenSearch' from the list of technologies. Then, hit the blue 'Next' button:

![](./img/name_and_opensearch.png)

Check the two boxes next to 'Add your current IP....' to add your current IP to the firewall rules.

![](./img/add_IP.png)

Next, select 'AI Search Plugin' from the plugins list.

![](./img/ai_search_plugin.png)

Then hit the blue 'Next' button at the bottom.

On the next page, scroll down to 'Data Node Selection', select 'Change Node Size'...

![](./img/node_selection.png)

...and select the m.80 sized node on the bottom

![](./img/node_size.png)

Then, hit the blue Next button. 

On the final screen, review all settings, then hit the blue Create Cluster button. 

![](./img/review.png)

And you've done it! Wait about ten minutes and you'll have an OpenSearch cluster on NetApp Instaclustr.