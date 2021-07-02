# How to use Amplify Auth in Nuxt JS

Vue JS is a frontend framework often extended with Nuxt JS to get great SSO value out of the box. AWS Amplify allows you to add authentication to your Vue web app with ease as shown in a previous article. In this article, I demonstrate how to add Cognito authentication with Amplify to a Nuxt web app.

![](https://cdn-images-1.medium.com/max/4000/1*KIt3rz0CJ-Iul_Ee1-VcQg.png)

## Why are we even using Nuxt JS and Amplify?

[Nuxt JS](https://nuxtjs.org/) extends upon [Vue JS](https://vuejs.org/) with the following useful features:

* Universal app means SSO value

* Static site generation

* Automatic route generation

[Amplify](https://github.com/aws-amplify/amplify-js) is an AWS framework which can be included in a Vue JS app to connect to AWS resources for Authentication, APIs plus much more. Amplify enables the use of [Congito](https://aws.amazon.com/cognito/) authentication, meaning the system can be serverless and makes it simple to add authorisation on APIs, too.

## The Setup

*Assuming the existence of a Congito User Pool:*

The basic structure of this project follows the steps of a Nuxt project

    'yarn create nuxt-app <project-name>'

Adding Amplify:

    yarn add aws-amplify @aws-amplify/ui-vue

## The Problem

In the tutorial for [Vue JS Amplify](https://docs.amplify.aws/), you add your configuration into 'main.js', but this isn’t a thing in Nuxt…

## The Solution

1. Add 'amplify.js' to '/plugins' in your Nuxt project

Configure this to match your setup — I have configured a Congito User Pool and an API which is only accessible to logged in users.

    import Vue from 'vue'
    import '@aws-amplify/ui-vue'
    import Amplify, { Auth } from 'aws-amplify'

    Amplify.configure({
      Auth: {
        region: 'EU-WEST-1',
        userPoolId: process.env.userPoolId,
        userPoolWebClientId: process.env.userPoolWebClientId,
        mandatorySignIn: false,
        oauth: {
          scope: ['email', 'openid'],
          redirectSignIn: `https://${process.env.rootDomain}/`,
          redirectSignOut: `https://${process.env.rootDomain}/`,
          responseType: 'code'
        }
      },
      API: {
        endpoints: [
          {
            name: 'UserAPI',
            endpoint: `https://${process.env.userApiDomain}`,
            custom_header: async () => {
              return { Authorization: `Bearer ${(await Auth.currentSession()).getIdToken().getJwtToken()}` }
            }
          }
        ]
      }
    })

    Vue.prototype.$Amplify = Amplify

2. Add the following snippet to your 'nuxt.config.js'

    plugins: [{ src: "~/plugins/aws-amplify.js", 'ssr: false' }]

## The Conclusion

Had I read the Nuxt docs better, I might have known how to do it.

The fun doesn’t stop here and you can add all of your favourite Vue JS modules this way, including [Vuetify](https://vuetifyjs.com/) and [Vue-Clipboard](https://github.com/Inndy/vue-clipboard2).

Or, go further with Nuxt and add modules like [Sitemap Generator](https://github.com/nuxt-community/sitemap-module).

## Thanks For Reading

I hope you have enjoyed this article. If you like the style, check out [T3chFlicks.org](https://t3chflicks.org) for more tech focused educational content ([YouTube](https://www.youtube.com/channel/UC0eSD-tdiJMI5GQTkMmZ-6w), [Instagram](https://www.instagram.com/t3chflicks/), [Facebook](https://www.facebook.com/t3chflicks), [Twitter](https://twitter.com/t3chflicks)).