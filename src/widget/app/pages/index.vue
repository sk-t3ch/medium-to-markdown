<template>
  <landing-page
    :name="serviceName"
    :endpoints="serviceEndpoints"
    :wide="wide"
    :second="second"
    :features="features"
    :examples="examples"
    :use-link="useLink"
    :description="description"
  />
</template>

<script>
import serviceConfig from '@/config/service.js'
import LandingPage from '~/components/LandingPage.vue'

export default {
  components: {
    LandingPage
  },
  data () {
    return {
      serviceName: serviceConfig.name,
      useLink: `${serviceConfig.t3chflicksRootDomain}/Using/${serviceConfig.slug}`,
      serviceEndpoints: serviceConfig.endpoints,
      description: serviceConfig.description,
      wide: `${serviceConfig.serviceRootDomain}/branding/coin.png`,
      second: `${serviceConfig.serviceRootDomain}/branding/apiPlay.png`,
      examples: serviceConfig.examples,
      features: serviceConfig.features
    }
  }
}
</script>
