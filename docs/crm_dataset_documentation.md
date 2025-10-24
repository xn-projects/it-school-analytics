# CRM Dataset Documentation

### 1. Calls

- **Id:** Unique identifier for each call.  
- **Call Start Time:** The exact time when the call started.  
- **Call Owner Name:** The name of the person responsible for the call.<br>
Possible values:<br>
`John Doe`, `Jane Smith`, `Alice Johnson`, `Bob Brown`, `Charlie Davis`, `Diana Evans`, `Ethan Harris`, `Fiona Jackson`, `George King`, `Hannah Lee`, `Ian Miller`, `Julia Nelson`, `Kevin Parker`, `Laura Quinn`, `Mason Roberts`, `Nina Scott`, `Oliver Taylor`, `Paula Underwood`, `Quincy Vincent`, `Rachel White`, `Sam Young`, `Tina Zhang`, `Ulysses Adams`, `Victor Barnes`, `Wendy Clark`, `Xander Dean`, `Yara Edwards`, `Zachary Foster`, `Amy Green`, `Ben Hall`, `Cara Iverson`, `Derek James`, `Eva Kent`.  
- **CONTACTID:** The unique identifier of the contact associated with this call.  
- **Call Type:** The type of the call.<br>
  Possible values:<br>
  `Inbound`, `Outbound`, `Missed`.  
- **Call Duration (in seconds):** Duration of the call measured in seconds.  
- **Call Status:** Final status of the call.<br>
  Possible values:<br>
  `Received`, `Attended Dialled`, `Unattended Dialled`, `Missed`, `Cancelled`, `Scheduled Unattended`, `Overdue`, `Scheduled Unattended Delay`, `Scheduled Attended`, `Scheduled Attended Delay`, `Scheduled`.  
- **Dialled Number:** The phone number that was dialed.  
- **Outgoing Call Status:** Status of the outgoing call. <br> 
  Possible values:<br>
  `Completed`, `Cancelled`, `Overdue`, `Scheduled`, `NaN`.  
- **Scheduled in CRM:** Indicates whether the call was scheduled through the CRM system.  
- **Tag:** A tag assigned to the call for categorization or tracking. 

---

### 2. Contacts

**Fields:**
- **Id:** Unique identifier of the contact.
- **Contact Owner Name:** The name of the person responsible for managing the contact.<br>
  Possible values:<br>
  `Rachel White`, `Charlie Davis`, `Bob Brown`, `Nina Scott`, `Alice Johnson`, `Ian Miller`, `Jane Smith`, `Julia Nelson`, `George King`, `Quincy Vincent`, `Diana Evans`, `Kevin Parker`, `Ulysses Adams`, `Victor Barnes`, `Yara Edwards`, `Paula Underwood`, `Mason Roberts`, `Ben Hall`, `Amy Green`, `Cara Iverson`, `Oliver Taylor`, `Eva Kent`, `Zachary Foster`, `Sam Young`, `Wendy Clark`, `Tina Zhang`, `Derek James`.
- **Created Time:** The date and time when the contact was added to the CRM database.
- **Modified Time:** The date and time when the contact record was last updated.
 
---

### 3. Spend

**Fields:**
- **Date:** The date when the impressions, clicks, and ad spend were tracked.
- **Source:** The platform or channel where the advertisement was displayed.<br>
  Possible values:<br>
  `Google Ads`, `Facebook Ads`, `CRM`, `Bloggers`, `Youtube Ads`, `SMM`, `Tiktok Ads`, `Organic`, `Telegram posts`, `Webinar`, `Offline`, `Partnership`, `Test`, `Radio`
- **Campaign:** The campaign under which the advertisement was shown.
- **Impressions:** The number of times the ad was shown to users.
- **Spend:** The amount of money spent on the advertising campaign or ad group during the specified period. 
- **Clicks:** The number of times users clicked on the ad.
- **AdGroup:** A subset within the campaign that contains one or more ads with shared targeting settings.
- **Ad:** The specific advertisement displayed to users.

---

### 4. Deals

**Fields:**
- **Id:** Unique identifier for each deal.
- **Deal Owner Name:** The name of the person responsible for managing the deal.<br>
  Posible values:<br>
  `Alice Johnson`, `Amy Green`, `Ben Hall`, `Bob Brown`, `Cara Iverson`, `Charlie Davis`, `Diana Evans`, `Eva Kent`, `George King`, `Ian Miller`, `Jane Smith`, `John Doe`, `Julia Nelson`, `Kevin Parker`, `Mason Roberts`, `Nina Scott`, `Oliver Taylor`, `Paula Underwood`, `Quincy Vincent`, `Rachel White`, `Sam Young`, `Ulysses Adams`, `Victor Barnes`, `Wendy Clark`, `Xander Dean`, `Yara Edwards`, `Zachary Foster`.
- **Created Time:** The timestamp indicating when the deal was created.
- **Course duration:** The duration of the course the student enrolled in.
- **Months of study:** The number of months the student has studied.
- **Closing Date:** The date when the deal was closed, if applicable.
- **Quality:** Classification of the deal’s quality, indicating its potential or target status.<br>
  Possible values:<br>
  `A – High`, `B – Medium`, `C – Low`,`D – Non Target`, `E – Non Qualified`, `F`
- **Stage:** The current stage of the deal in the sales process.<br>
  Possible values:<br>
  `Call Delayed`, `Free Education`, `Lost`, `Need a Consultation`, `Need To Call`, `Need to Call – Sales`, `New Lead`, `Payment Done`, `Qualified`, `Registered on Offline Day`, `Registered on Webinar`, `Test Sent`, `Waiting For Payment` 
- **Lost Reason:** The reason the deal was lost, if applicable.<br>
  Possible values:<br>
  `Changed Decision`, `Conditions are`, ` Considering a different`, `Didn’t leave an`, `Does not know how to`, `Does not speak English`, `Doesn’t Answer`, `Duplicate`, `Expensive`, `Gutstein refusal`, `Inadequate`, `Invalid number`, `Needs time to think`, `Next stream`, `Non target`, `Not for myself`, `Refugee`, `Stopped Answering`, `The contract did not fit`, `Thought for free`, `Went to Rivals`
- **Page:** The web page or landing page where the lead  was acquired.<br>
  Possible values:<br>
  `/test — Usually used for test pages created by developers or marketers to verify functionality, conduct A/B testing, or run experimental page launches.`<br>
  `/ppc — Indicates a page associated with Pay-Per-Click (PPC) advertising. This is typically a landing page for visitors who came through paid contextual ads.`<br>
  `/page1 — Likely represents a sequentially numbered page that can be used for various purposes, such as multi-step forms or surveys.`<br>
  `/ — Represents the root (main) page of the website — the homepage loaded through the primary domain.`<br>
  `/account — A page intended for the user’s personal account, where they can manage their data, deals, or orders.`<br>
  `/eng/test — Similar to /test, but for the English-language version of the website, typically used for testing English-specific functionality or layouts.`
- **Campaign:** The name or code of the marketing campaign associated with the deal.
- **SLA:** The service-level agreement time, indicating the expected response time.
- **Content (Ad):** The specific ad shown to users.
- **Term (AdGroup):** A subset within the campaign containing ads with shared targeting settings.
- **Source:** The origin of the lead<br>
  Possible values:<br>
  `Facebook Ads — The lead was obtained through advertising on Facebook. This may include contextual ads or sponsored posts clicked by users.`<br>
  `Organic — The lead came through organic search, meaning the user found the website or landing page via a search engine (e.g., Google) without paid advertising.`<br>
  `Telegram posts — The lead originated from posts or publications on the Telegram messenger, such as channel or group posts.`<br>
  `Google Ads — The lead came from Google’s advertising platform through contextual or display ads run via Google Ads.`<br>
  `YouTube Ads — The lead was acquired via advertising on YouTube, such as video ads shown before or during videos.`<br>
  `CRM — Indicates that the lead was generated through internal CRM processes, possibly from internal data, repeat contacts, or automated funnels.`<br>
  `Webinar — The lead was generated through participation in a webinar — an educational or promotional online event.`<br>
  `SMM — The lead came through social media marketing (SMM), meaning promotion through social networks without specifying a particular platform.`<br>
  `TikTok Ads — The lead came through advertising on the TikTok platform, using short video ads to attract the audience.`<br>
  `Bloggers — The lead originated from collaborations with bloggers or influencers who mentioned the product or service in posts, videos, or reviews.`<br>
  `Partnership — The lead was generated through partnerships or collaborations with other companies or organizations.`<br>
  `Test — Indicates a test source, meaning the lead was generated as part of a test campaign or experiment.`<br>
  `Offline — The lead came through offline sources such as personal meetings, events, conferences, or other non-digital interactions.`<br>
  `NaN — Represents an empty value, meaning no data is available about the lead source.`
- **Payment Type:** The method of payment used or expected from the client.<br>
  Possible values:<br>
  `One Payment`, `Recurring Payments`, `Reservation`
- **Product:** The specific product or service related to the deal.<br>
  Possible values:<br>
  `Data Analytics`, `Digital Marketing`, `Find Yourself in IT`, `UX/UI Design`, `Web Developer`
- **Education Type:** The type of education associated with the deal.<br>
  Possible values:<br>
  `Morning`, `Evening`
- **Initial Amount Paid:** The initial payment made by the client.
- **Offer Total Amount:** The total value of the offer presented to the client.
- **Contact Name:** The identifier of the contact person associated with the deal.
- **City:** The city related to the client.
- **Level of Deutsch:** The client’s German language proficiency level, if applicable.

  ---
