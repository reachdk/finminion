library(readr)
citi <- read_csv("~/Google Drive/finminion/citi_master.csv")
citi$Date <- as.Date(citi$Date, format="%d-%m-%y")
View(citi)

# build parsing tokens

homeloan <- "R.A.C.P.C."
cab <- "PayTm|PAYTM|UBER"
cafe <- "COFFEE DAY|STARBUCKS|CHAI POINT|BARISTA"
cash <- "WITHDRAWAL"
creditcard <- "XX9753"
entertainment <- "Netflix|Bookmyshow|PVR|V BANGALO"
familysocial <- "CORNER HOUS|FUNCITY|DUNKIN"
grocery <- "SPENCERS|FAMILIES|NAMDHARI|MORE MEGASTORE|urdoorstep.com|Aishwarya"
imps1 <- "XXXXXXXXXXX4682"
imps2 <- "XXXXXXX7579"
impsnani <- "XXXXXXXXXXX0796"
impsvajjar <- "XXXXXXX1286"
impsmama <- "XXXXXXX0162"
impssibu <- "XXXXXXX0436"
medical <- "DR SUNNY|LIFE LINE|LEVINE|St Johns|EYE FOUNDATION|Eye Foundation"
school <- "GYAN|AKSHARA"
sharekhan <- "SSKI"
shop <- "AMAZON|myntra|"
social <- "TIPSY|GREENS BAR|BLISTERING BARNACLES|BREWSKY|FISHERMANS|BLACK PEARL|FOOD PILIGRIM|FENNYS|HOOT"
utilities <- "SPECTRANET"

# Add a class field to the data, default "other"
citi$class <- "Other"

# Add a month field for aggregation
citi$month <- as.Date(cut(citi$Date, breaks="month"))

#Subset to include only expenses
exp <- subset(citi, citi$Withdrawals > 0)
View(exp)

# Apply the regexp and return their class
exp$class <- ifelse(grepl(homeloan, exp$Description), "Home Loan", 
                     ifelse(grepl(impsmama, exp$Description), "Mama",
                            ifelse(grepl(social, exp$Description), "Social",
                                   ifelse(grepl(cab, exp$Description), "Cab",
                                          ifelse(grepl(cash, exp$Description), "Cash",
                                                 ifelse(grepl(cafe, exp$Description), "Cafe",
                                                        ifelse(grepl(creditcard, exp$Description), "Card",
                                                               ifelse(grepl(entertainment, exp$Description), "Entertainment",
                                                                      ifelse(grepl(familysocial, exp$Description), "Family Social",
                                                                             ifelse(grepl(medical, exp$Description), "medical",
                                                                                    ifelse(grepl(grocery, exp$Description), "grocery",
                                                                                           ifelse(grepl(imps1, exp$Description), "imps1",
                                                                                                  ifelse(grepl(imps2, exp$Description), "imps2",
                                                                                                         ifelse(grepl(impsnani, exp$Description), "impsnani",
                                                                                                                ifelse(grepl(impsvajjar, exp$Description), "impsvajjar",
                                                                                                                       ifelse(grepl(impssibu, exp$Description), "impssibu",
                                                                                                                              ifelse(grepl(school, exp$Description), "school",
                                                                                                                                     ifelse(grepl(shop, exp$Description), "shop",
                                                                                                                                            ifelse(grepl(utilities, exp$Description), "utilities", "Other")))))))))))))))))))
                                                                                                                            

# Build summary table of monthly spend per class
library(plyr)
smr <- ddply(exp, .(month, class), summarise, cost=abs(sum(Withdrawals)))

# look for trends over the year by fitting a statistical model
# Not Working - library(ggplot2)
# Not Working - ggplot(smr, aes(month, cost, col=class)) +
# Not Working -   facet_wrap(~class, ncol=2, scale="free_y") +
# Not Working -   geom_smooth(method="loess", se=F) + geom_point() +
# Not Working -   theme(axis.text.x=element_text(angle=45, hjust=1),
# Not Working -         legend.position="none") +
# Not Working -   labs(x="", y="Monthly total (£)")

# mean monthly spend per class
yl <- ddply(smr, .(class), summarise, m=mean(cost))

library(ggplot2)
ggplot(yl, aes(x=class, y=m)) +
  geom_bar(stat="identity") +
  labs(y="Average monthly expense (£)", x="")

#aggregate by class and month
exp_aggregate <- aggregate(x = exp['Withdrawals'], by = exp[c('class', 'month')], FUN = sum)
