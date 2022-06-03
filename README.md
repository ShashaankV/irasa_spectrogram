# irasa_spectrogram

Extension of the IRASA method for time-varying spectral analyses. 

## Description

Time series such as EEG consist of oscillatory- and aperiodic-type activity. These represent different processes on interest. Aperiodic are likened to fractal series and power-law spectra, where there is broad decline in the power spectrum that follows a 1/frequency<sup>x</sup> function. IRASA is a method for taking a raw spectrum and estimating two new spectra - aperiodic and oscillatory spectra. 

IRASA (Irregular Resampling Auto-Spectral Analysis) is a method for separating these components. In brief, it uses the self-affine property of fractal series where up- or down- sampling such series results in similar statistical properties. The power spectrum is one of these properties. For a purely fractal (w/ aperiodic 1/f spectrum), the spectrum is preserved but with a change in scale. This scale is given by h<sup>H</sup>, where h is the resampling factor and H is called the <a href=https://en.wikipedia.org/wiki/Hurst_exponent target="_blank"></href> Hurst exponent</a>. With a mixed oscillatory and aperiodic signal, up- and down- sampling can be used to shift the osc component while preserving the aperiodic component. Taking the inner product of such shifted spectra results in an attenuation of the osc component while preserving the aperiodic. To achieve this the h<sup>H</sup> scaling factor has to be accounted for. IRASA achieves this by using h, 1/h reciprocal pairs this canceling the h<sup>H</sup> factor. 

In practice (see /notebook/example.ipynb) this works fairly well based on our predictive modeling results. However, there are some artifacts to be aware off. First, IRASA often adds small artifactual oscillatory peaks to the aperiodic estimate resulting in "negative osc power". These peaks are the "average" of the shifted true osc peaks. Second, there are edge effects. Aperiodic and oscillatory spectra should be analyzed within bands somewhat away from the band limits of the original signal. Near these extrema, baseline artifacts are introduced. This is important to note for preprocessing that uses bandpass filters. We recommend bandpassing after IRASA is implemented.  

Motivation -  IRASA spectrogram extends work by 


## Table of Contents

<!-- If your README is long, add a table of contents to make it easy for users to find what they need. -->

- [Installation](#installation)
- [Usage](#usage)
- [Tests](#tests)


## Installation

<!-- What are the steps required to install your project? Provide a step-by-step description of how to get the development environment running. -->

## Usage

<!-- Provide instructions and examples for use. Include screenshots as needed.

To add a screenshot, create an `assets/images` folder in your repository and upload your screenshot to it. Then, using the relative filepath, add it to your README using the following syntax:

    ```md
    ![alt text](assets/images/screenshot.png) -->
    ```

## Credits

Cite this paper if used in .. 

## License

<!-- The last section of a high-quality README file is the license. This lets other developers know what they can and cannot do with your project. If you need help choosing a license, refer to [https://choosealicense.com/](https://choosealicense.com/). -->

<!-- ## Badges

![badmath](https://img.shields.io/github/languages/top/lernantino/badmath)

Badges aren't necessary, per se, but they demonstrate street cred. Badges let other developers know that you know what you're doing. Check out the badges hosted by [shields.io](https://shields.io/). You may not understand what they all represent now, but you will in time.

## Features

If your project has a lot of features, list them here.

## How to Contribute

If you created an application or package and would like other developers to contribute it, you can include guidelines for how to do so. The [Contributor Covenant](https://www.contributor-covenant.org/) is an industry standard, but you can always write your own if you'd prefer. -->

## Tests

Go the extra mile and write tests for your application. Then provide examples on how to run them here.
