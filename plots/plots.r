library(Cairo)

#vierership by time evening games
broadcastData %>% 
  filter(lubridate::minute(broadcastTime) > 00 & lubridate::minute(broadcastTime) <= 17 & lubridate::hour(broadcastTime) == 19 & broadcastTime > '2018-04-01') %>% 
  group_by(showID,minute = lubridate::minute(broadcastTime)) %>% 
  summarise(averageWatchers = mean(watching)) %>% 
  ggplot(aes(x=minute, y=averageWatchers, group = showID)) + geom_line(alpha = 1/8, colour = 'red', size = 1) + theme(legend.position="none") + 
  theme_minimal(base_size=15, base_family="Impact") +
  labs(title="Viewership Over Time (Evening Games)",
       subtitle="Viewership is max by minute by game",
       x="Game Minute",
       y="Viewership",
       caption=""
  )  + 
  theme(
    plot.subtitle = element_text(color="#AAAAAA", size=10),
    plot.title = element_text(family="Impact", size = 20),
    plot.caption = element_text(color="#AAAAAA", size=18)
  ) 

#viewership by time afternoon games
broadcastData %>% 
  filter(lubridate::minute(broadcastTime) > 00 & lubridate::minute(broadcastTime) <= 17 & lubridate::hour(broadcastTime) == 13 & broadcastTime > '2018-04-01') %>% 
  group_by(showID,minute = lubridate::minute(broadcastTime)) %>% 
  summarise(averageWatchers = mean(watching)) %>% 
  ggplot(aes(x=minute, y=averageWatchers,group = showID)) + geom_line(alpha = 1/8, colour = 'red', size = 1) + theme(legend.position="none") + 
  theme_minimal(base_size=15, base_family="Impact") +
  labs(title="Viewership Over Time (Afternoon Games)",
       subtitle="Viewership is max by minute by game",
       x="Game Minute",
       y="Viewership",
       caption=""
  )  + 
  theme(
    plot.subtitle = element_text(color="#AAAAAA", size=10),
    plot.title = element_text(family="Impact", size = 20),
    plot.caption = element_text(color="#AAAAAA", size=18)
  ) 

#downloads by day and big announcements
downloadAnalysis %>% ggplot(aes(x=date,y=totalDownloads, colour=sponsored)) + geom_point() + scale_x_date(date_breaks = "1 month",date_labels = "%b") + 
  geom_vline(xintercept = as.numeric(as.Date("2018-03-04")), linetype=4) +
  geom_vline(xintercept = as.numeric(as.Date("2018-03-25")), linetype=4) +
  geom_vline(xintercept = as.numeric(as.Date("2018-02-18")), linetype=4) +
  geom_vline(xintercept = as.numeric(as.Date("2017-12-24")), linetype=4) +
  geom_text(aes(x=as.Date("2018-03-25"), label="\nReady Player One Announcement", y=40000), colour="blue", angle=90, text=element_text(size=11)) +
  geom_text(aes(x=as.Date("2018-02-18"), label="\n25k Prize", y=40000), colour="blue", angle=90, text=element_text(size=11)) + 
  geom_text(aes(x=as.Date("2018-03-4"), label="\n50k Prize", y=40000), colour="blue", angle=90, text=element_text(size=11)) + 
  geom_text(aes(x=as.Date("2017-12-24"), label="\n24k Prize", y=40000), colour="blue", angle=90, text=element_text(size=11)) +
  theme_minimal(base_size=15, base_family="Impact") +
  labs(title="Total Downloads by Day - Key Events",
       subtitle="total downloads by day - colored by sponsored games",
       x="Date",
       y="Total Downloads",
       caption=""
  )  + 
  theme(
    plot.subtitle = element_text(color="#AAAAAA", size=10),
    plot.title = element_text(family="Impact", size = 20),
    plot.caption = element_text(color="#AAAAAA", size=18)
  ) 

# distribution of how many people win the game
questionAnswerData %>% 
  group_by(showID) %>% 
  slice(which.max(questionNumber)) %>% 
  filter(questionNumber >= 12 & isCorrect == "True", count <= 5000) %>%
  ggplot(aes(count)) + geom_histogram(binwidth = 100, fill = 'red') +
  theme_minimal(base_size=15, base_family="Impact") +
  labs(title="Distribution of Winners Each Game",
       subtitle="Outliers Removed",
       x="Winning Players",
       y="Game Count",
       caption="")  + 
  theme(
    plot.subtitle = element_text(color="#AAAAAA", size=10),
    plot.title = element_text(family="Impact", size = 20),
    plot.caption = element_text(color="#AAAAAA", size=18),
    legend.position="none")

#density of winners  by game
payoutData %>% 
  group_by(showID) %>% 
  filter(n() < 5000) %>% 
  count() %>% 
  ggplot(aes(n)) + geom_density(fill = 'red', colour = 'red', alpha = .54) +
  theme_minimal(base_size=15, base_family="Impact") +
  labs(title="Density of Winners Each Game",
       subtitle="Density Plot",
       x="Winning Players",
       y="Density",
       caption="")  + 
  theme(
    plot.subtitle = element_text(color="#AAAAAA", size=10),
    plot.title = element_text(family="Impact", size = 20),
    plot.caption = element_text(color="#AAAAAA", size=18),
    legend.position="none")

#average correct percent over time
questionAnswerData %>% 
  group_by(date,questionID) %>% 
  summarise(totalCount = sum(count),
            correctCount = sum(count[isCorrect == "True"]),
            pcntCorrect = correctCount/totalCount) %>% 
  summarise(avgPcntCorrect = mean(pcntCorrect)) %>% 
  ggplot(aes(date,avgPcntCorrect)) + geom_line(size = 1, colour = 'red') + geom_smooth() +
  scale_x_date(date_breaks = "1 month",date_labels = "%b") +
  theme_minimal(base_size=15, base_family="Impact") +
  labs(title="Average Correct % by Question and Game",
       subtitle="",
       x="Date",
       y="Avg Pcnt Correct",
       caption="")  + 
  theme(
    plot.subtitle = element_text(color="#AAAAAA", size=10),
    plot.title = element_text(family="Impact", size = 20),
    plot.caption = element_text(color="#AAAAAA", size=18),
    legend.position="none")

#average winnings over time
payoutData %>%
  group_by(date = as.Date(broadcastTime)) %>% 
  summarize(avgWinnings = round(mean(prize),2)) %>% 
  filter(avgWinnings < 200) %>% 
  ggplot(aes(date,avgWinnings)) + geom_line(colour = 'red', size = 1) +
  geom_smooth() +
  scale_x_date(date_breaks = "1 month",date_labels = "%b") +
  theme_minimal(base_size=15, base_family="Impact") +
  labs(title="Average Winning Amount Over Time",
       subtitle="Outliers Removed - Average by Day",
       x="Date",
       y="Average Winnings",
       caption=""
  )  + 
  theme(
    plot.subtitle = element_text(color="#AAAAAA", size=10),
    plot.title = element_text(family="Impact", size = 20),
    plot.caption = element_text(color="#AAAAAA", size=18)
  ) 

#max players over time

totalViewersbyDay %>% 
  filter(maxPlayers < 3000000) %>% 
  ggplot(aes(x=date,y=maxPlayers)) + geom_line(size = 1, colour = 'red') + geom_smooth() +
  scale_x_date(date_breaks = "1 month",date_labels = "%b") +
  theme_minimal(base_size=15, base_family="Impact") +
  labs(title="Max Players Over Time",
       subtitle="Viewership is max by game",
       x="Broadcast Date",
       y="Viewership",
       caption=""
  )  + 
  theme(
    plot.subtitle = element_text(color="#AAAAAA", size=10),
    plot.title = element_text(family="Impact", size = 20),
    plot.caption = element_text(color="#AAAAAA", size=18)
  ) 

#category difficulty 
pcntCorrectDF <- questionAnswerData %>% 
  filter(showID %in% twelveShows) %>% 
  group_by(category) %>% 
  filter(!is.na(category)) %>% 
  summarise(totalCount = sum(count),
            correctCount = sum(count[isCorrect == "True"]),
            pcntCorrect = correctCount/totalCount,
            gameCount = n_distinct(showID)) %>% 
  filter(totalCount != 701562) %>% 
  select(category,pcntCorrect,correctCount, totalCount, gameCount) %>% 
  arrange(desc(pcntCorrect)) 

pcntCorrectDF %>% 
  filter(gameCount > 20) %>% 
ggplot(aes(reorder(category, -pcntCorrect),pcntCorrect)) + geom_col()



#most frequent categories 
questionData %>% 
  group_by(category) %>% 
  summarise(n = n()) %>% 
  arrange(desc(n)) %>% 
  filter(category != '') %>% 
  ggplot(aes(reorder(category, -n),n)) + geom_col(fill = 'red') +
  theme_minimal(base_size=15, base_family="Impact") +
  labs(title="Frequency of Question Categories",
       subtitle="",
       x="Categories",
       y="Category Count",
       caption="")  + 
  theme(
    plot.subtitle = element_text(color="#AAAAAA", size=10),
    plot.title = element_text(family="Impact", size = 20),
    plot.caption = element_text(color="#AAAAAA", size=18),
    legend.position="none")


questionData %>% 
  group_by(category) %>% 
  summarise(n = n()) %>% 
  mutate(pcntTotal = n/sum(n)) %>% 
  arrange(desc(pcntTotal)) %>%filter(n >= 208) %>% 
  summarise(totalPcnt = sum(pcntTotal))

questionData %>% 
  group_by(category) %>% 
  summarise(n = n()) %>% 
  mutate(pcntTotal = n/sum(n)) %>% 
  arrange(desc(pcntTotal)) %>%filter(n >= 274) %>% 
  summarise(totalPcnt = sum(pcntTotal))



#categories by difficulty 
questionAnswerData %>% 
  filter(showID %in% twelveShows) %>% 
  group_by(category) %>% 
  filter(!is.na(category)) %>% 
  summarise(totalCount = sum(count),
            correctCount = sum(count[isCorrect == "True"]),
            pcntCorrect = correctCount/totalCount,
            gameCount = n_distinct(showID)) %>% 
  filter(totalCount != 701562) %>% 
  select(category,pcntCorrect,correctCount, totalCount, gameCount) %>% 
  arrange(desc(pcntCorrect)) 




CairoWin()
#word frequencies over time
chatWords %>% 
  mutate(chatTime = as.Date(lubridate::ymd_hms(chatTime))) %>% 
  group_by(chatTime, word) %>% 
  summarize(wordCount = n()) %>% 
  filter(word %in% c('glitch','scott','birthday','love')) %>% 
  ggplot(aes(x=chatTime, y=wordCount, group = word, color = as.factor(word))) + geom_line(alpha = 1, size = 1) + theme(legend.position="none") + 
  theme_minimal(base_size=15, base_family="Impact") +
  labs(title="Word Frequency Over Time",
       subtitle="Top 4 Words in Chat",
       x="Date",
       y="Word Count",
       caption=""
  )  + 
  theme(
    plot.subtitle = element_text(color="#AAAAAA", size=10),
    plot.title = element_text(family="Impact", size = 20),
    plot.caption = element_text(color="#AAAAAA", size=18)
  ) 


#meme frequency
chatWords %>% 
  mutate(chatTime = as.Date(lubridate::ymd_hms(chatTime))) %>% 
  group_by(chatTime, word) %>% 
  summarize(wordCount = n()) %>% 
  filter(word %in% c('soup','wakanda','dab')) %>% 
  ggplot(aes(x=chatTime, y=wordCount, group = word, color = as.factor(word))) + geom_line(alpha = 1, size = 1) + theme(legend.position="none") + 
  theme_minimal(base_size=15, base_family="Impact") +
  labs(title="Word Frequency Over Time",
       subtitle="Top Memes",
       x="Date",
       y="Word Count",
       caption=""
  )  + 
  theme(
    plot.subtitle = element_text(color="#AAAAAA", size=10),
    plot.title = element_text(family="Impact", size = 20),
    plot.caption = element_text(color="#AAAAAA", size=18)
  ) 
