Title: Correcting digit bias in customer survey data
Date: 2015-03-21
Tags: statistics, data
Slug: digit_bias_correction
Status: draft

Surveying customers or a sample of a population as part of an experiment can provide important insight into the opinions, 
behaviors, or experiences that people have. In some cases surveys are the only feasible option for measuring something in a
scalable and unbiased way. But the data that results can be filled with errors and skewed by the biases of the respondents.
In this post I will be discussing one particular form of bias that is common in survey data that I will refer to as
**digit bias** or **digit preference**. This form of bias is common when respondents are asked to provide a numerical 
value as a part of the survey, e.g. their weight, a time duration for an event, etc. 

Digit bias can arise due to a natural tendency to round values to a nearest multiple of 5 or 10, or due to skewed 
perceptions. How would you respond if you were asked "What time did you get to work this morning?" Most people would 
have a tendency to respond in multiples of 15 or 30 minutes, e.g. 8:30 even if they truly arrived at 8:23. Perhaps 
different people would have a tendency to over or under estimate depending on who was asking the question or what the 
assumed reaction might be? If you are expected to be at work by 9:00 and 
arrive at 9:13, you might round that back to 9:00 either to try to deceive the person asking the question or out of 
guilt for having been late. Conversely, one who was early might not think to round their answer as strongly, maybe 
only to th nearest multiple of 5 minutes.

I was recently working with some survey data, particularly focused on a question about a length of time of service, where
digit bias was clearly evident. A histogram of the data showed an overwhelming tendency to round responses to a
multiple of 5 minutes (the response is given as an integer number of minutes up to 999). Even more than that, after
binning the data into 5 minute intervals, there was a secondary tendency to prefer multiples of 15 minutes, e.g. an
answer of 45 minutes was significantly more prevalent than 40 or 50 minutes.

Ultimately we were interested in the distribution of the time durations reported in the survey, and I wanted to find a 
way to correct this very obvious bias present in the data because I suspected that it had the overall effect of skewing 
the distribution.

In researching ways of handling this particular issue, I found an excellent 2008 paper by Camarda, Eilers, and Gampe, 
["Modelling general patterns of digit preference"](http://www.demogr.mpg.de/publications%5Cfiles%5C2945_1235560583_1_Camarda-Feb09-Sage.pdf)
that provided a model for measuring and correcting such biases in data.

One of the reasons why I found the paper so useful was that the authors actually published their code as a package in 
R. 