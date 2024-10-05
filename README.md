# Seismic Detection Across the Solar System
### By Luyu Wu - High School Student at University of Toronto Schools


## Problem Statement
Planetary seismology missions struggle with the power requirements necessary to send continuous seismic data back to Earth. But only a fraction of this data is scientifically useful! Instead of sending back all the data collected, what if we could program a lander to distinguish signals from noise, and send back only the data we care about? Your challenge is to write a computer program to analyze real data from the Apollo missions and the Mars InSight Lander to identify seismic quakes within the noise!

## Approach
I decided to use a purely algorithmic approach to this challenge. This is due to my physics background and interest in finding solutions that are not machine learning (and thus black-box) based.


## Process
First, I was interested in analyzing the frequency data. I thought it might be possible to isolate an earthquake using a frequency signature (maybe dependent on the bodies radius and density).

![WithoutWithQuake](https://github.com/user-attachments/assets/ad05466d-cde1-44e4-a938-6dd100627af5)

Here you can see the preliminary analysis.

Seeing that the pre-earthquake signal is primarily composed of sub-Hertz frequencies, we can implement a high-pass filter to remove thise noise.

![HighPass](https://github.com/user-attachments/assets/b19280ce-51f8-457c-9c3d-93d67e1e70fd)

Here you can see the signal before and after the high-pass signal.

Having cleaned up the signal, I decided to use a moving-box average, with a small and large box. This was outlined in the tutorial as a common algorithm. The ratio of these two boxes across time has useful information for the change in rate of the change in magnitude of seismic activity. A visualization of this can be seen below.

![initialmodel](https://github.com/user-attachments/assets/2e6c3501-52ab-494b-a0b0-7a0b74fb8263)


However, I soon found out that this algorithm was not very good. Finding the ratio was very sensitive to low-amplitude fast changes in seismic activity. Instead, I decided to use the difference of the absolute-value average of the two boxes. This gave better results as visible below.

![model](https://github.com/user-attachments/assets/596571cd-e360-484c-971d-21e17fda10cf)

By using this model, and running it over the training data (lunar dataset), we can graph out the difference (residuals) between our model and the labeled time of earthquake.

![Residuals](https://github.com/user-attachments/assets/55fdea33-0e41-40b9-9a14-9cde7e740f32)

As is visible, there are some significant outliers.
By graphing and analyzing this data, I realized this was caused by the earthquake being too early in the dataset. Since we are doing a box average, this means our algorithm doesn't notice the rising change in those cases.
To fix this, we add a buffer zone equal to our larger box appended before our data. This gives significantly better results as visible here.

![new_resiuals](https://github.com/user-attachments/assets/8bb82164-4df5-4bf8-80b6-5bc42b26fcdd)

I checked the remaining outliers by graphing out the testing datasets with residuals > 1e+3, and the results can be seen here:

![image](https://github.com/user-attachments/assets/3543378a-cbbf-4afc-9ca5-f89b83e2565c)

As visible above, all of these have large residuals are not because of false positives. They are caused by multiple seismic events in the data collection window.
In fact, many of the results from my are qualitatively more accurate than the catalog labeled trigger times.


## Works Cited

Nagao, T., Takeuchi, A., Nakamura, K., & Anonymous. (2011). A new algorithm for the detection of seismic quiescence; introduction of the RTM algorithm, a modified RTL algorithm. Earth, Planets, and Space, 63(3), 315–324. https://doi.org/10.5047/eps.2010.12.007

  Cuellar, A., Suarez, G., & Espinosa-Aranda, J. M. (2017). Performance evaluation of the earthquake detection and classification algorithm 2(tS-tP) of the Seismic Alert System of Mexico (SASMEX). Bulletin of the Seismological Society of America, 107(3), 1451–1463. https://doi.org/10.1785/0120150330
