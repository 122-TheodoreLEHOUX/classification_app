#This is a classification app on streamlit

The app is divided by the following : 
    - pages folder : contains all pages of the app. The description of what the page should do is commentated in each page code
    - tools : differents class to handle connection with db, handling of data

Goal : app to classify text by filling colums FiClassifcation FailureType RepairStatus CompCardChanged Notes. To be deploy as an .exe file

Pages descriptions :
- Index (to rename depending on web habits) home page, permit to filter the db and classify it
- Chart : Page with filter which will display chart (tbd)
- Parameter : Page to configure your app.

DB architecture
One table : RepairReportTable
Contains columns : OrderType	operation_type	Notification	OS	RmaNumber	Reference	Designation	ReceiptDate	SerialNumber	Project	ReturnNumber	WorkCenter	Location	TypeOfWork	SortingZone	histo_location	age_location	CSContact	lead_time	RepairReport	ClientFailureDescription	FiClassifcation	FailureType	RepairStatus	CompCardChanged	Notes
