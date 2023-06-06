# makeYourChoice
Progetto di backend per l'esame "Progettazione e Produzione Multimediale", Laurea Triennale in Ingegneria Informatica presso l'Università degli Studi di Firenze.

## Key features
- [x] Users can select topics that are interested in by subscribing to "categories".
- [x] Users can search and follow other users to see all of their surveys without filters.
- [x] After a survey has reached its deadline, it only remains accessible to the user that created it through the page "Manage my surveys".
- [x] When a survey is about to expire and a user still hasn't taken it, a message appears informing the user about the imminent deadline.
- [x] When a user deletes its account all its data is safely removed and statistics are updated.
- [x] **If a user opens a link to take a survey without being logged in, he/she is redirected to the login page. After logging in, the user is redirected to the survey page.**
- [x] **If a user opens a link to take a survey without being registered, he/she is redirected to the login page. If the user clicks on the register button, he/she is redirected to the registration page and after the registration is completed, the user is redirected to the survey page.**

## Security measures
1. You cannot force an action by trying to access a page that you are not allowed to access. For example, if you are not logged in and/or you aren't the owner of a survey, you cannot delete it by accessing the "Delete Survey" page and passing the survey id as a parameter in the browser url bar.
2. The Secret Key is passed as an environment variable, so it's not visible in the source code.
3. Before a critical action is performed, a confirmation message is displayed to the user.
4. When a survey is deleted, all the related questions and choices are deleted as well.
5. When a category is deleted, all the related surveys are deleted as well.
6. When a user is deleted, all the related surveys are deleted as well.
7. When a user is deleted, all the related subscriptions are deleted as well.

## Instructions

### Take surveys
1. Before you can take a survey, you need to subscribe to a category of interest or follow a user. To do that, you can press the Subscribe button in the main page or in the Manage categories page to see the list of categories that you can subscribe to. You can also press the Search button in the Search user page to see the list of users that you can follow. Then you can press the Follow button to follow a user.
2. To take a survey, you can press the Take button in the main page or in the Manage surveys page to see the list of surveys that you have created.

### Create surveys
1. Register or login to the website.
2. To create a new survey it's necessary to verify whether the category already exists or not. If it doesn't exist, you can create it by pressing Manage categories. If it exists, you can select it from a list during the creation of the survey.
3. After creating a survey, you can add questions to it by pressing Add Questions.
4. After adding questions, you can add choices to each question by pressing Add Choices.

### Manage surveys
1. To manage surveys, you can press the Manage surveys page to see the list of surveys that you have created.
2. In the Manage surveys page, you can delete a survey by pressing the Delete button, or you can see the results of a survey by pressing the Results button.

### Manage categories
1. To manage categories, you can press the Manage categories page to see the list of categories that you have created.
2. In the Manage categories page, you can delete a category by pressing the Delete button. Note that you can only delete a category only if you have created it.
3. In the Manage categories page, you can create a category by pressing the Create a new category button.

### Search user
1. To search a user, you can visit the Search user page. If you want to list all the users, you can press the Search button without entering any username.
2. You can follow a user by pressing the Follow button.
3. You can see the list of users that you are following by pressing the Followed users button. To unfollow a user, you can press the Unfollow button.

