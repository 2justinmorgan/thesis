# Master's Thesis

**Link** <br>
[![Digital Commons Link](https://justinleemorgan.com/digital_commons_thesis_link.svg)](https://digitalcommons.calpoly.edu/theses/2304)

**Title** <br>
Clustering Web Users By Mouse Movement to Detect Bots and Botnet Attacks

**Author** <br>
Justin Morgan

**Degree** <br>
MS in Computer Science

**Department** <br>
Computer Science

**College** <br>
College of Engineering

**Committee** <br>
Franz Kurfess, Ph.D. - _chair_ <br>
Phoenix (Dongfeng) Fang, Ph.D.  <br>
Maria Pantoja, Ph.D.  <br>

**Summary** <br>
This thesis research provides an **unsupervised learning** approach to detect a bot or machine browsing a website. By utilizing Golang's **parallelization** and scalability through **distribution**, a web user's mouse movement is efficiently extracted and analyzed in real time. An added benefit of this web **bot detection** scheme is that it does not require users to login or prove their humanness with programs such as CAPTCHA. As a result of this research, several mouse movement **features sets** that have shown to be useful to differentiate users. Also included is a **membership bias metric** that measures how well a clustering method differentiates users.

**Abstract** <br>
The need for website administrators to efficiently and accurately detect the presence of web bots has shown to be a challenging problem. As the sophistication of modern web bots increases, specifically their ability to more closely mimic the behavior of humans, web bot detection schemes are more quickly becoming obsolete by failing to maintain effectiveness. Though machine learning-based detection schemes have been a successful approach to recent implementations, web bots are able to apply similar machine learning tactics to mimic human users, thus bypassing such detection schemes. This work seeks to address the issue of machine learning based bots bypassing machine learning-based detection schemes, by introducing a novel unsupervised learning approach to cluster users based on behavioral biometrics. The idea is that, by differentiating users based on their behavior, for example how they use the mouse or type on the keyboard, information can be provided for website administrators to make more informed decisions on declaring if a user is a human or a bot. This approach is similar to how modern websites require users to login before browsing their website; which in doing so, website administrators can make informed decisions on declaring if a user is a human or a bot. An added benefit of this approach is that it is a human observational proof (HOP); meaning that it will not inconvenience the user (user friction) with human interactive proofs (HIP) such as CAPTCHA, or with login requirements
