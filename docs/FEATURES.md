# Goodreads App Features Overview

This document outlines the core features of our book management application, inspired by Goodreads. While we draw from Goodreads’ successful functionalities, our app offers a modern, streamlined experience tailored to readers who want to track, discover, and share their reading journey.

## Books

Each book entry in the app provides rich information and interactive features. The system is designed to help users manage their reading journey with clarity and ease.

### Book Details

Every book includes the following attributes:

* **Cover Image** – Displays the book’s cover. If unavailable, a default placeholder with the app logo is used.
* **Title** – The full title of the book.
* **Author(s)** – One or more authors associated with the book.
* **Number of Pages** – Essential for tracking reading progress.
* **ISBN** – A unique identifier for cataloging.
* **Publication Date** – The original date of publication.

### Book Statistics

Each book displays key community engagement metrics:

* **Average User Rating** – Calculated from all user-submitted ratings (e.g., 4.2/5).
* **Total Number of Ratings** – Indicates how many users have rated the book.
* **Readers Count** – Shows how many users have added the book to any shelf (e.g., “Read,” “Currently Reading”).

### User Interactions

Users can perform the following actions with any book:

* **Quick Add to Shelf** – One-click option to add a book to the “Want to Read” shelf.
* **Shelf Selector Dropdown** – Expandable menu to choose another shelf, such as:

  * *Currently Reading*
  * *Read*
  * *Custom Shelves* (e.g., "Favorites", "Abandoned", "To Reread")
* **Move or Remove from Shelves** – Easily reassign a book to a different shelf or remove it altogether.
* **Rate and Review** – Users can rate and review books once they’ve marked them as “Read.”
* **Add or Edit Reading Dates** – Users can specify or modify the start and end dates of their reading period.
* **Track Progress** – For books marked as “Currently Reading,” users can update their progress by entering how many pages they’ve read.

## Shelves

Shelves allow users to organize their books according to reading status or personalized categories. This system offers both flexibility and clarity in managing one’s reading journey.

### Default Shelves

Every user begins with three built-in shelves:

* **Want to Read** – For books the user intends to read.
* **Currently Reading** – For books the user is actively reading. Enables progress tracking.
* **Read** – For books the user has completed. Enables features like rating, reviewing, and tracking reading dates.

These shelves are system-defined and cannot be renamed or deleted to maintain consistency across the platform. Each book can be placed on only one default shelf at a time.

### Custom Shelves

Users can create additional shelves to suit their preferences, reading goals, or organization style. Examples include:

* *Favorites*
* *To Reread*
* *Abandoned*
* *2025 TBR*

Books can be added to multiple custom shelves simultaneously, allowing for more nuanced organization beyond default status-based shelving.

### Shelf Management

The app supports comprehensive shelf control:

* **Create and Name Custom Shelves** – Users can freely create shelves with meaningful or thematic labels.
* **Edit or Delete Custom Shelves** – Custom shelves can be renamed or removed at any time.
* **Assign Books to Shelves** – Users can move books between default shelves and tag them with multiple custom shelves without losing progress or metadata.
* **Filter by Shelf** – Users can filter their collection to display books from a specific shelf.
* **Sort Books Within Shelves** – Books can be sorted by:

  * Date added
  * Title (A–Z or Z–A)
  * Author
  * Personal rating
  * Average community rating
  * Date started or finished (if applicable)

## Reviews

Reviews allow users to reflect on their reading experience and share opinions with the community. They also help others discover books that match their interests—or avoid those that don't.

### Writing a Review

Users can write a review once a book is added to the **Read** shelf. A review may include:

* **Rating** – A required star-based rating from 1 to 5 stars.
* **Text Review** – An optional field for sharing thoughts, summaries, critiques, or quotes.
* **Spoiler Tag** – Users can mark sections of their review as spoilers. These are hidden by default unless a reader clicks *see spoiler*.
* **Publication/Edit Date** – The date the review was written or last updated is displayed.

### Editing and Managing Reviews

* **Edit Review** – Users can update the rating, text, or spoiler tags at any time.
* **Delete Review** – Users can permanently delete a review if they choose.

### Review Visibility

* **Public by Default** – Reviews are visible to all users and appear on the book’s detail page.
* **Private Option** – Users can mark a review as private, making it visible only to themselves.
* **Sorting Options** – On a book’s page, reviews can be sorted by:

  * Most liked
  * Most recent
  * Highest rating
  * Lowest rating

### Community Feedback

* **Like Reviews** – Users can like others’ reviews to express agreement or appreciation.
* **Comment on Reviews** – (Optional feature) Users may comment on reviews to discuss opinions or ask follow-up questions.

## User Profiles

User profiles serve as personal hubs for tracking reading activity, showcasing reviews, and managing social features within the app. Each profile reflects the user's unique reading journey and preferences.

### Profile Overview

Each user profile displays:

* **Username and Profile Picture** – Customizable identity for each user.
* **Bio** – Optional short description to share interests or favorite genres.
* **Total Books Read** – Count of all books marked as “Read.”
* **Currently Reading** – A glance at books the user is actively reading.
* **Recent Activity** – Includes recent ratings, reviews, or shelf changes.
* **Custom Shelves** – View and browse all custom shelves the user has created.

### Reading Goals & Progress

Users can set a yearly reading goal and track progress directly from their profile.

* **Set Annual Goal** – Users define how many books they aim to read within the current calendar year.
* **Progress Bar** – Visual tracker shows how many books have been read toward the goal.
* **Timeline Tracking** – Displays whether the user is ahead, behind, or on track based on current reading pace.
* **Completion History** – Keeps a record of past goals and their outcomes (optional).

### Social Features

* **Friends List** – Displays mutual connections or followed users.
* **Follow Users** – Users can follow others to stay updated on their activity.
* **Profile Privacy Settings** – Choose between public, friends-only, or private visibility.

### Profile Customization

* **Edit Profile Info** – Users can change their bio, profile picture, and display name.

## Notifications

Notifications keep users informed and engaged by providing timely updates related to their books and activities within the app. Users can customize their notification preferences to ensure they receive relevant alerts.

### Types of Notifications

* **Review Interactions** – Alerts when:
  * Someone likes or comments on a review the user has posted.
  * A review receives a reply or is flagged for being reported.

* **Friend Activity** – Notifications about the user's friends' activities, such as:
  * A friend adding or completing a book.
  * A friend's review or rating.

### Customizing Notifications

Users can fine-tune their notification preferences:

* **Push Notifications** – Users can opt to receive push notifications for specific activities, such as when someone comments on a review.

### Notification Control

* **Mute Specific Notifications** – Users can mute notifications for certain books, shelves, or activities.
* **Do Not Disturb Mode** – Temporarily disable all notifications for a set period.
* **Notification History** – A log of past notifications that users can revisit at any time.

## Recommendations

The recommendation system helps users discover new books aligned with their interests, reading history, and community trends. It encourages continued engagement and exploration of new genres, authors, and titles.

### Personalized Recommendations

The app suggests books based on:

* **Reading History** – Titles similar to books the user has marked as "Read" or rated highly.
* **Shelves & Genres** – Recommendations reflect books from genres or shelves the user frequently interacts with (e.g., “Fantasy,” “Classics,” or “Non-fiction”).
* **Favorite Authors** – Suggestions for other titles from favorite authors.

### Community-Driven Suggestions

Users receive curated suggestions powered by community behavior:

* **Trending Books** – Popular books currently being read, reviewed, or rated across the app.
* **Friends’ Picks** – Books highly rated or shelved by friends.
* **Readers Like You** – Suggestions based on users with similar reading patterns or ratings.

### Discover Page

A dedicated section for exploration, featuring:

* **Editor’s Picks** – Hand-selected recommendations across categories.
* **Friends' Favorites** – Upcoming or newly published books by genre or interest.
* **Hidden Gems** – Highly rated titles for user with similar patterns.

### Customization & Feedback

* **Mark as Not Interested** – Users can remove books from future recommendations.
* **Rate to Improve** – Encouragement to rate more books to refine recommendation accuracy.
* **Genre Preferences** – Users can select preferred or disliked genres to shape suggestions.
* **Dynamic Learning** – The more users interact with books (rating, shelving, reviewing), the more accurate and tailored their recommendations become.
