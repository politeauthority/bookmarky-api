# Bookmarky Api v0.0.1.66
Self hosted open source bookmark tool

## Features
 - Add bookmarks

### Organize
 - Through recently added
 - Through recently clicked
 - Through folders

## Bookmarky Parts
 - [Bookmarky Api](https://github.com/politeauthority/bookmarky-api)
 - [Bookmarky Web (Simple)](https://github.com/politeauthority/bookmarky-web-simple)
 - [Bookmarky Extensions](https://github.com/politeauthority/bookmarky-extensions)
 - [Polite Lib](https://github.com/politeauthority/polite-lib)

## Development
### Process
 - Branch from `stage` branch
 - Merge to `stage`
 - Merge `stage` to `main`
 - Delete `stage` branch on Github
 - Run `task ci-new-stage` locally

### To Dos

### General
 - Ensure cicd update-version Tasks works for `api` and `web`

#### Plugin
 - Add visual understanding of failure or success
 - Learn how to store credentials and fetch token on request
 - Figuee out why https://www.youtube.com/watch?v=lhlRHOxMNys&t=1s wont save

#### Api
 - Fix slug generation for instances like "News - Internation" becomining "news---international"
 - Make Tag slugs unique to user
 
 
 ### Web
 - FIX UPDATE-VERSION task to touch README.md! 
 - Add back manual Bookmark creation
 - Add confirmation on Tag Add modal creation
 - Add keyboard focus for Tag Add modal
 - - Most Used Tags is not ordered by use
   - Should include metric of use
- BUG: on search load gif never dissapears
- Bug with Loading MORE from recent bookmarks
- BUG: Links arent always opening in new tab ie (search)
- BUG: Links open in new tab ALWAYS
- 