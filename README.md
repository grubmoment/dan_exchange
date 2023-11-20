This project is run the same way that Finance was. The zip file can be opened in vscode for broswer and run on the locally hosted GitHub server.

Registration and logging in is the same as before. This was not a central focus of the project, so I found it sufficient to keep. After logging in, you will see a logo, and four buttons labeled tickets, textbooks, dorm, sell, and ledger.

The logo acts as a link to the home page. This is where a user is able to see all of the items that they have listed on the Exchange. The items that they have listed for sale are divided into categories.

The ticket page is where users are able to buy tickets. It currently supports buying football tickets since have the highest demand and are the most likely to reach a secondary market. On the tickets page, a user is able to see all of the football games that have tickets being resold. You will be able to see the opponent, the game date, and the lowest asking price fo the ticket. If you press on the button to the right, you will be able to see all of the tickets with their associated seller, contact information, and asking price shown. It was originally intended to only show games with the opponent that was clicked, but there were many roadblocks when trying to accomplish this. This will be discussed more in DESIGN.md.

The textbooks page is where users can buy used textbooks. Users post a picture of the cover, their asking price, and their contact information. The process for uploading images does require a few steps. I used this method on advice of a TA. Once you find a picture for the cover of your book or after you take a picture of your book, save the image onto your computer. Then, save that image to Google Drive. Drive will give the option to share which will provide a sharing link. Make sure your permission is anyone can view and then copy the link. The link must be converted to a usable format using the instructions detailed on this page: https://dev.to/temmietope/embedding-a-google-drive-image-in-html-3mm9. There is also a Codepen project that does this automatically: https://codepen.io/DrewJaynes/details/abJNNjb. This codepen project is a little buggy, I found that it truncates the full converted links at times when it encounters and underscore. This link can then be pasted into the image field for textbooks, and it will be posted to the page.

The usage of dorm-items is virtually the same as textbooks with the only difference being the option to upload a caption.

Sell is the tab you go to to list all of the items you want to sell. There are three buttons for tickets, textbooks, and dorm items. Each button leads to its respective form that needs to be filled out to list the item.

Video: https://youtu.be/mBRmyjkZeYM