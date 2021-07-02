
# 🚫 Users Only: Quickstart for creating a SaaS pt. 1 — User Management

Managing users and API keys is a necessary task for creating a Software as a Service (SaaS). In this article, I demonstrate how to create a simple, cost effective serverless SaaS user management application. The frontend is created using Vue JS and the Amplify plugin. The backend uses Cognito for authentication of the user management API, and a key system created with DynamoDB which authorises users to access a test API created with Application Load Balancer. Check out the live demo 💽.

![](https://cdn-images-1.medium.com/max/4000/1*9RH_PC5EM5l0fM9wnEE97Q.png)

Not everything is intended for everyone. In a scenario where restricting access is necessary, user management must become a component of the architecture. The AWS solution to user management is the [Cognito](https://aws.amazon.com/cognito/) service. This integrates simply with [API Gateway](https://aws.amazon.com/api-gateway/) — but as described in the previous article, API gateway can get pretty expensive, and for high load the more cost effective alternative is [Application Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html).
[**Cheaper than API Gateway — ALB with Lambda using CloudFormation**
*An alternative to API gateway is Application Load Balancer. ALB can be connected with Lambda to produce a highly…*medium.com](https://medium.com/@t3chflicks/cheaper-than-api-gateway-alb-with-lambda-using-cloudformation-b32b126bbddc)

The architecture for this user management application (see below) makes use of both API gateway and ALB for their respective benefits. API gateway is chosen for the User API for two reasons:

* the requests are likely to be low in volume meaning costs will be low

* the requests are direct from the frontend with authentication using the Amplify package with the Vue JS framework

ALB is chosen for the example service Test API as it is expected to experience a high volume of requests which might rack up a hefty bill on API Gateway. Also, the requests are likely to be from other servers meaning API keys are preferable. Users are generated an API key on sign up which is used to authenticate the Test API. Usage of the API is monitored by incrementing a count on the User table each time a request is made to the Test API.

![User Manager Quickstart Architecture Diagram](https://cdn-images-1.medium.com/max/2000/1*X5y3CnFO29vNlm9E65W8Aw.png)*User Manager Quickstart Architecture Diagram*

This architecture is cost effective for high-load APIs. A quote from this [article](https://serverless-training.com/articles/save-money-by-replacing-api-gateway-with-application-load-balancer/) might help you decide if your service falls into that category:
> # $15 (ALB’s cost) worth of API Gateway calls will net you around 4.3 million API calls in the month (well, 5.3 million if you count the free tier). So, if your API is small enough to fit under that number of calls, stick with API Gateway — it’s simpler to use. But, 5.3 million API calls is only around two requests per second. So, if your API is used very much at all — or even if you have DNS health checks enabled — you could easily end up paying more for API Gateway than you would for Application Load Balancer.

I presume this article will not bring in more than two reads per second, meaning an ALB would not be suitable for running the demo of the service. Instead, the test API seen in the diagram has been replaced with another API Gateway. You can see a demonstration of the app in use below.
> # [The full code for this project can be found here ☁️](https://github.com/sk-t3ch/AWS-user-manager-app-quickstart)
> # [The live demo can be found here 💽](https://um-app.t3chflicks.org)

![Video of Use Manager App](https://cdn-images-1.medium.com/max/2000/1*d0DiGLhhjM9U6nh80BX2-A.gif)*Video of Use Manager App*

## Let’s Build! 🔩

## Backend

The infrastructure for this system is written as code using the [CloudFormation](https://aws.amazon.com/cloudformation/) framework.

### VPC

ALBs must be placed within a Virtual Private Cloud on AWS. The service uses a stripped down VPC consisting of only two public subnets and an Internet Gateway. A more complete VPC is described in a previous article:
[**Virtual Private Cloud on AWS — Quickstart with CloudFormation**
*A Virtual Private Cloud is the foundation from which to build a new system. In this article, I demonstrate how to…*medium.com](https://medium.com/swlh/virtual-private-cloud-on-aws-quickstart-with-cloudformation-4583109b2433)

### User Management with Cognito

The AWS Cognito service is used to manage users. Users are stored in user pools, and Clients (mobile or web apps) can interact with them using an API. I configured the Cognito user pool to send an email with a verification code on sign up.

<iframe src="https://medium.com/media/36649a5848d147a53e8b63abcc0001c3" frameborder=0></iframe>

You must also define a client; this allows for OAuth on our frontend client.
> NB: Setting the URLs to localhost allows for local development.

<iframe src="https://medium.com/media/3833b22e688c1a4db9847f8b23041236" frameborder=0></iframe>

Cognito user pools offer useful event tiggers such as sign up confirmation. I have used the post-confirmation event to trigger a Lambda function which writes the user’s username, a newly generated API key, and a zero initialised counter to a DynamoDB table. The table has a Global Secondary Index (GSI) on the Key attribute which allows for a user lookup with just the Key.

<iframe src="https://medium.com/media/f86c87270808a62347773f89a57a9ee5" frameborder=0></iframe>

The PostConfirmation Lambda function template:

<iframe src="https://medium.com/media/2e36839a8fcf9cf9bf230d98781fbd86" frameborder=0></iframe>

The PostConfirmation Lambda is a Python function which creates an API key and stores it in the DynamoDB table:

<iframe src="https://medium.com/media/866e9049984f1d953e8b9b2bd4041ff6" frameborder=0></iframe>

### User API

Endpoints created for users to access their profile and generate an API key are authenticated for the logged in user. Authentication is easily added to API gateway with Cognito (CORS are set open for development purposes).

<iframe src="https://medium.com/media/25a2ed8b5217248266118b58de078590" frameborder=0></iframe>

The code for getting and generating keys is very similar to the post-confirmation Lambda code.

### Service API — Test

The API I’ve created with ALB is for the high traffic volume endpoints which are authenticated using an API key. This API key is sent in a POST request to the service.

<iframe src="https://medium.com/media/75af5a7dd0a0c16736911898ecd12efc" frameborder=0></iframe>

The service uses the user’s API key for a query on a GSI of the user table to get the username and Count, then increment the Count and return the updated Count. Again, I have added open CORS whilst developing. For security, these should been locked down.

<iframe src="https://medium.com/media/dd5d450f41ec03f35b3e739440d27a21" frameborder=0></iframe>

## Frontend

### Vue JS

My choice of JavaScript framework is [Vue JS](https://vuejs.org/) and I make quite a lot of use of [Vuetify](https://vuetifyjs.com/en/components/api-explorer/), a [Material Design](https://material.io/design/) styling framework. After installing, it’s as simple as:

    vue create frontend
    ---step through configurations and use defaults
    vue add vuetify

### Amplify

[AWS Amplify](https://docs.amplify.aws/start) is a JS plugin which consists of some useful functions for serverless Auth and API, as well as some frontend components for Vue JS, enabling user authentication flows.

<iframe src="https://medium.com/media/15bea24a98f3ec63c838efa6d9c5d04c" frameborder=0></iframe>

In the Vue App, I use Amplify’s Authenticator UI components for user authentication flows.

<iframe src="https://medium.com/media/a170a39fb82ae1225f0b1bab57691eba" frameborder=0></iframe>

This is what an authenticated user sees:

![Unauthenticated User Page](https://cdn-images-1.medium.com/max/6720/1*Nm-uo8rlpu3dK2sCR12ZwQ.png)*Unauthenticated User Page*

With the API configured in main.js, calling an API inside a Vue component is pretty simple.

<iframe src="https://medium.com/media/6aa1070c57efa1c0f89c155a5990a2b0" frameborder=0></iframe>

The authorisation header is set for the current logged in user. The code for accessing the User API is just as clean.

<iframe src="https://medium.com/media/9f920d2c0b2509e4c93e2aa818fe32de" frameborder=0></iframe>
> # [full code ☁️ ](https://github.com/sk-t3ch/AWS-user-manager-app-quickstart). . . . . . . . . . . . . . . . . . . . . . . . . . .[live demo 💽](https://um-app.t3chflicks.org)

## Deploy

Using CloudFormation templates mean it is simple to deploy this infrastructure using the AWS CLI.

    aws cloudformation deploy --template-name ./00-infra.yml

Vue JS builds a static site which is uploaded to S3 and deployed using CloudFront.

    npm run build;
    aws s3 cp ./dist s3://<< your bucket name >> --recursive

![Video of Use Manager App](https://cdn-images-1.medium.com/max/2000/1*d0DiGLhhjM9U6nh80BX2-A.gif)*Video of Use Manager App*

### After Thoughts

This Architecture is the basis for a SaaS, the next step is to link to a payment service such as Stripe to handle subscriptions, which is done in part 2:
[**💸 Pay Me: Quickstart for creating a SaaS pt.2 — Stripe Payments**
*Creating a SaaS solution is fun, but creating a payment system can be a minefield. In this article, I demonstrate how…*medium.com](https://medium.com/@t3chflicks/pay-me-quickstart-for-creating-a-saas-pt-2-stripe-payments-44bc4bb8388e)

Some popular APIs from [Rapid API Top 100](https://rapidapi.com/blog/mos):
> [URL Shortener Service](https://rapidapi.com/BigLobster/api/url-shortener-service) — [Learn More](https://rapidapi.com/blog/most-popular-api/#url-shortener-service)
> [Investors Exchange (IEX) Trading](https://rapidapi.com/eec19846/api/investors-exchange-iex-trading) — [Learn More](https://rapidapi.com/blog/most-popular-api/#investors-exchange-iex-trading)
> [Crime Data](https://rapidapi.com/jgentes/api/crime-data) — [Learn More](https://rapidapi.com/blog/most-popular-api/#crime-data)
> [Youtube To Mp3 Download](https://rapidapi.com/CoolGuruji/api/youtube-to-mp3-download) — [Learn More](https://rapidapi.com/blog/most-popular-api/#youtube-to-mp3-download)
> [Web Search](https://rapidapi.com/contextualwebsearch/api/web-search) — [Learn More](https://rapidapi.com/blog/most-popular-api/#web-search)
> [JokeAPI](https://rapidapi.com/Sv443/api/jokeapi) — [Learn More](https://rapidapi.com/blog/most-popular-api/#jokeapi)
> [Genius](https://rapidapi.com/brianiswu/api/genius) — [Learn More](https://rapidapi.com/blog/most-popular-api/#genius)
> [Crypto Asset Tickers](https://rapidapi.com/BraveNewCoin/api/crypto-asset-tickers) — [Learn More](https://rapidapi.com/blog/most-popular-api/#crypto-asset-tickers)

## Thanks for reading

I hope you have enjoyed this article. If you like the style, check out [T3chFlicks.org](https://t3chflicks.org/Projects/aws-saas-quickstart) for more tech-focused educational content ([YouTube](https://www.youtube.com/channel/UC0eSD-tdiJMI5GQTkMmZ-6w), [Instagram](https://www.instagram.com/t3chflicks/), [Facebook](https://www.facebook.com/t3chflicks), [Twitter](https://twitter.com/t3chflicks)).
> # [The full code for this project can be found here ☁️](https://github.com/sk-t3ch/AWS-user-manager-app-quickstart)
> # [The live demo can be found here 💽](https://um-app.t3chflicks.org)

<iframe src="https://medium.com/media/2c6af79d78f2aec12e0c3a0f7654bae0" frameborder=0></iframe>

Resources:

* [https://chaosgears.com/lets-start-developing-using-vue-and-amplify/](https://chaosgears.com/lets-start-developing-using-vue-and-amplify/)

* [https://docs.amplify.aws/lib/auth/getting-started/q/platform/js](https://docs.amplify.aws/lib/auth/getting-started/q/platform/js)

* [https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification.html](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification.html)

* [https://www.youtube.com/watch?v=7dQZLY9-wL0](https://www.youtube.com/watch?v=7dQZLY9-wL0)
