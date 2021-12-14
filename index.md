<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

## Number of Patients Registered at GP Practices in London 

The NHS is currently experiencing some of the most severe pressures in its 70-year history and GP surgeries across the country are experiencing significant rising demand for services while struggling to recruit staff [[1]](https://www.bma.org.uk/advice-and-support/nhs-delivery-and-workforce/pressures/pressures-in-general-practice).

As outlined by NHS England in the [General Practice Forward View](https://www.england.nhs.uk/gp/gpfv/), there is an increasing need to implement new innovative ways of delivering primary care at scale. One possible solution is GP practice mergers. Mergers, typically, involve two or more neighbouring practices coming together to pool resources and staff while increasing patient list size and accordingly practice income [[2]](https://www.england.nhs.uk/south/wp-content/uploads/sites/6/2015/12/guide-mergers-gp.pdf).

This page tracks the number of patients registered at individual GP Practices, with a focus on practices in the [London Commissioning Region](https://www.england.nhs.uk/commissioning/).

Data sources: [NHS Digital](https://digital.nhs.uk/data-and-information/publications/statistical/patients-registered-at-a-gp-practice) and [NHS Prescription Services](https://digital.nhs.uk/services/organisation-data-service/file-downloads/gp-and-gp-practice-related-data) 

<hr class="nhsuk-u-margin-top-0 nhsuk-u-margin-bottom-6">

{% include update.html %}

<div class="nhsuk-warning-callout">
  <h3 class="nhsuk-warning-callout__label">
    Data Quality<span class="nhsuk-u-visually-hidden">:</span>
  </h3>
  <p>The outbreak of Coronavirus (COVID-19) has led to changes in the work of General Practices and consequently data collection initiatives by NHS Digital. Until activity in this healthcare setting stabilises, conclusions drawn from these data should take into consideration the country's circumstances. GP practices in London are defined as any practice falling within the London Commissioning Region (Y56) with an active status. Babylon Healthcare’s online GP at Hand practices (GP Practice Code: E85124 and Y06487) are excluded from the analyses. 
  </p>
</div>

### Number of patients registered at indvidual GP Practices 

{% include plotly_obj.html %}

### Number of patients registered at indvidual GP Practices in London

<p>
Each circle marker on the map represents a GP practice. Click on an indvidual marker for the GP practice name, code, address, contact information and the number of patients registered at the practice. 
</p>

<iframe width= "900" height="700"  src="assets/folium/folium_obj.html" style="border:none;"></iframe>

<div class="nhsuk-action-link">
  <a class="nhsuk-action-link__link" href="assets/data/gp_pop_london_mapped_final.csv">
    <svg class="nhsuk-icon nhsuk-icon__arrow-right-circle" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M0 0h24v24H0z" fill="none"></path>
      <path d="M12 2a10 10 0 0 0-9.95 9h11.64L9.74 7.05a1 1 0 0 1 1.41-1.41l5.66 5.65a1 1 0 0 1 0 1.42l-5.66 5.65a1 1 0 0 1-1.41 0 1 1 0 0 1 0-1.41L13.69 13H2.05A10 10 0 1 0 12 2z"></path>
    </svg>
    <span class="nhsuk-action-link__text">Download this dataset (.csv)</span>
  </a>
</div>

## About this page

This page is built using end-to-end open source analytical tools including: [The NHS Digital Service Manual](https://service-manual.nhs.uk/), [python](https://nhs-pycom.net/), [plotly](https://plotly.com/python/), [folium](http://python-visualization.github.io/folium/), [geopy](https://geopy.readthedocs.io/en/stable/), [beautiful soup](https://www.crummy.com/software/BeautifulSoup/), [github.io](https://pages.github.com/), and [github actions](https://github.com/features/actions).

<div class="nhsuk-action-link">
  <a class="nhsuk-action-link__link" href="https://github.com/nhsx/open-analytics-template">
    <svg class="nhsuk-icon nhsuk-icon__arrow-right-circle" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M0 0h24v24H0z" fill="none"></path>
      <path d="M12 2a10 10 0 0 0-9.95 9h11.64L9.74 7.05a1 1 0 0 1 1.41-1.41l5.66 5.65a1 1 0 0 1 0 1.42l-5.66 5.65a1 1 0 0 1-1.41 0 1 1 0 0 1 0-1.41L13.69 13H2.05A10 10 0 1 0 12 2z"></path>
    </svg>
    <span class="nhsuk-action-link__text">Find out how to build your own open analytics pipeline</span>
  </a>
</div>

If you have any suggestions or questions, email: <a href="mailto:mattia.ficarelli@nhsx.nhs.uk">mattia.ficarelli@nhsx.nhs.uk</a>

<hr class="nhsuk-u-margin-top-0 nhsuk-u-margin-bottom-6">
