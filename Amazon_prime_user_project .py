#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np 
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt 


# In[2]:


Amazon = pd.read_csv(r'C:\Users\tilum\OneDrive\Desktop\amazon_prime_users.csv')


# In[3]:


Amazon.head()


# In[4]:


Amazon.columns


# In[5]:


Amazon.info()


# In[6]:


Amazon.shape


# In[7]:


Amazon.isnull().sum()


# In[8]:


Amazon_copy = Amazon.copy()


# In[9]:


len(Amazon[Amazon.duplicated()])


# In[10]:


#  this dataset has no null /duplicated values


# In[11]:


dup_email = Amazon[Amazon.duplicated(subset=['Email Address'], keep= False)]


# In[12]:


dup_email.head()


# In[13]:


len(dup_email)


# In[14]:


len(Amazon['Email Address'])- len(Amazon['Email Address'].drop_duplicates())

# finding duplicate emails


# In[15]:


len(Amazon['Email Address'])
# Total number of emails


# In[16]:


len(Amazon['Email Address'].drop_duplicates())
# These are unique emails


# In[17]:


# I won't remove the duplicated emails since they have different date of births. 
# I will just ignore them for the analysis purposes


# In[18]:


from datetime import  datetime 


# In[19]:


# Now, I will convert the date of birth to age


# In[20]:


Amazon['Date of Birth']= Amazon['Date of Birth'].apply(pd.to_datetime)


# In[21]:


Amazon.info()
# checking if the column has converted to datetime lm,j9


# In[22]:


date_today = datetime.now()


# In[23]:


date_year = date_today.year


# In[24]:


Amazon['Users_age']= date_year - Amazon['Date of Birth'].dt.year


# In[25]:


Amazon['Users_age'].head()


# In[26]:


# Let's do some descriptive statistics


# In[27]:


Amazon['Users_age'].mean()


# In[ ]:





# In[28]:


Q1= Amazon['Users_age'].quantile(0.25)
Q3= Amazon['Users_age'].quantile(0.75)

print(Q1,Q3)

IQR= Q3-Q1

print(IQR)

lower_bound= Q1-1.5*IQR
upper_bound= Q3+1.5*IQR

print('lower_bound:', lower_bound,'upper_bound:',upper_bound)

# now identify the outliers- 
outliers = Amazon[(Amazon['Users_age']< lower_bound)|(Amazon['Users_age']>upper_bound)]


# In[29]:


Amazon.loc[Amazon['Users_age']<0, 'Users_age']= 54


# In[30]:


import matplotlib.pyplot as plt 


# In[31]:


sns.boxplot(Amazon['Users_age'])
plt.show()


# In[32]:


Amazon.head()


# In[33]:


Amazon.info()


# In[34]:


# So, the targeted age(50% of the data) is between 37 and 73. 


# In[35]:


def age_category(Amazon):
    Amazon['Users_age_category']= pd.cut(x=Amazon['Users_age'],bins=[0,37,73,129],labels = ['young','targeted_age','old'])
    return Amazon


# In[36]:


age_category(Amazon)


# In[37]:


# encoding Engagemnet metrics 


# In[38]:


Amazon['Engagement Metrics']= Amazon['Engagement Metrics'].replace(['Low','Medium','High'],[1,2,3])


# In[39]:


Amazon


# In[40]:


Amazon.groupby(['Users_age_category'])['Engagement Metrics'].sum().sort_values(ascending= False).reset_index()


# # Targeted age group has double engagement than other two age segments. supports my hypothesis

# In[41]:


# SECOND OBJ


# In[42]:


# Analyze how subscription types (auto/manual) affect Amazon Prime’s business opportunities


# In[43]:


fig1 = px.histogram(Amazon, x='Usage Frequency', 
                   color='Renewal Status',
                   barmode='group',
                   title = 'Renewal Status vs. Usage Frequency')
fig1.show()


# In[44]:


# Purchase history-categorize


# In[45]:


plt.rcParams['figure.figsize']=8,8

labels = Amazon['Purchase History'].value_counts().index.tolist()
sizes = Amazon['Purchase History'].value_counts().tolist()
explode = (0, 0.1)

plt.pie(sizes, labels = labels,  autopct = '%1.1f%%',startangle = 90,textprops ={'fontsize': 14})


# In[46]:


fig1 = px.histogram(Amazon, x='Renewal Status', 
                   color='Purchase History', title ='Renewal Status vs. Purchase History',
                   barmode='group')
fig1.show()


# In[47]:


group = Amazon.groupby('Renewal Status')


# In[48]:


purchase_count = group['Purchase History'].count()


# In[49]:


purchase_count


# ## Electronics and books are higher in demand for auto renewal users. 
# 
# ## Auto renewal users buying more product
# 
# ## From the purchase history, it shows that 
# ## clothing is in demand among manual users. As a marketing startegy 
# ## may be we can give those customers discount offers with auto renewals. 
# 
# 

# In[50]:


# 3rd obj


# In[51]:


fig1 = px.histogram(Amazon, x='Engagement Metrics', color= 'Subscription Plan', title ='Subscription Plan vs. Engagement Metrics',
                   barmode='group')
fig1.show()


# In[52]:


# Annual subscription plan users have the highest engagement Metrics


# In[53]:


fig1 = px.histogram(Amazon, x='Usage Frequency', 
                   color='Subscription Plan',
                   barmode='group',
                   title= 'Subscription Plan vs Usage Frequency')
fig1.show()


# In[54]:


# Annual subscription plan users are the most frequent users


# In[55]:


Amazon.groupby(['Subscription Plan','Usage Frequency'])['Purchase History'].count().sort_values(ascending= False).reset_index()


# # After analyzing time based trends , it shows that Annual and frequent users made the highest amount of purchase. 
# ## Area of opportunity- Monthly subscribers with regular and frequent usage 

# In[56]:


Amazon['Feedback/Ratings'].min()


# In[57]:


Amazon['Feedback/Ratings'].max()


# In[58]:


Amazon['Feedback/Ratings'].mean()


# In[62]:


Amazon.groupby(['Subscription Plan','Usage Frequency'])['Feedback/Ratings'].mean().sort_values(ascending= False).reset_index()


# In[ ]:





# # According to the avg feedback/ratings, the biggest area of opportunity would be Monthly regular/occasional usage users because they give the highest ratings. It will be easier to convert their subscription to annual from monthly. 
# 

# In[60]:


Amazon.to_csv(r'C:\Users\tilum\OneDrive\Desktop\amazon_prime_users.csv', index = False)


# In[ ]:




