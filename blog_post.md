# Giving away free APIs without going broke.

I like to write articles on Medium. I also want to share the same articles on our own site without having to rewrite them in a different format. For this reason, I have created a service which runs something similar to the Medium-To-MarkDown library, a programme which converts Medium posts to MarkDown format. I have offered it to everyone on our site.


To be clear, [Medium-To-MarkDown](https://t3chflicks.org/Services/medium-to-markdown) is an example service whilst we work out how best to run an effective Software as a Service (SAAS).

In this article, we:

* Break down the hosting costs of the service

* Determine how feasible it really is to give away free APIs

* Discuss some tactics to avoid going broke

![](https://cdn-images-1.medium.com/max/4000/1*h_mDgR5Iq0TXLy0zoofTMQ.png)

### What do we want?

* To send an article URL and in response get the [MarkDown](https://www.markdownguide.org/)

* To share this service with the world

* To avoid T3chFlicks going into financial meltdown

We want to use this service and render the MarkDown on our site for the posts we write. We typically write one article each month, so we can’t really justify the purpose of an API. Instead, a better solution might be to execute a script for the conversion when building our site.

However, at T3chFlicks **we want to share** - our only opposition is financial. This is a fairly simple service, running on AWS (the largest Cloud Hosting company). Surely this wouldn’t be too much for a UK-based tech company?

## The Architecture

![](https://cdn-images-1.medium.com/max/4200/1*rDHR5nwVHfdZvKgOy6X09A.png)

The architecture diagram above shows a user making a request to the `MediumToMarkDown/Convert` endpoint on the load balancer. The [Application Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html) (ALB) sends this event to the API [Lambda](https://aws.amazon.com/lambda/), which responds immediately with a URL for the location of the MarkDown article result. The API Lambda also puts the Medium-To-MarkDown job into a [SQS](https://aws.amazon.com/sqs/) queue to be consumed by the Processing Lambda.

The Processing Lambda is where all the work is done, and the result is written to an [S3](https://aws.amazon.com/s3/) Bucket which is attached to a [CloudFront](https://aws.amazon.com/cloudfront/) distribution. This has a lifecycle policy set to delete after one day.

The Medium-To-MarkDown processing script is pretty simple and can be found [here](https://gist.github.com/sk-t3ch/71c480017d844789841978d43c9be5b0).

### The Interface

We made a widget that allows users to easily play with the API and view the [JSON schemas](https://json-schema.org/) which define the input and output:

![T3chFlicks API-Play Widget](https://cdn-images-1.medium.com/max/6348/1*kWO_ZW35SLGhj689nURGrw.png)
*T3chFlicks API-Play Widget*

The programmatic use of the API is as follows:

    curl --location --request POST 'https://api.t3chflicks.org/medium-to-markdown/convert' \
    --header 'Content-Type: application/json' \
    --data-raw '{
    "mediumURL": "https://t3chflicks.medium.com/how-to-use-amplify-auth-in-nuxt-js-4dbf07da7033",
    "key": "52d9204da6c6f8cefd13fb43384c365656dc091473634e3b701892e3cc29abef7af4a8de1f3913235bd4b56a409e09597400da67e358cd62e118d3922563791e"
    }'
    >>> {"location": "https://document-store.t3chflicks.org/medium-to-markdown/document-title"}

Accessing the MarkDown document:

    curl https://document-store.t3chflicks.org/medium-to-markdown/document-title

    >>> "# How to use Amplify Auth in Nuxt JS \nVue JS is a frontend framework often extended with Nuxt JS to get great SSO value out of the box. AWS Amplify allows you to add authentication to your Vue web app with ease as shown in a previous article. In this article, I demonstrate how to add Cognito authentication with Amplify to a Nuxt web app..."
> # [🤖 The widget can be found on our site 🤖](https://t3chflicks.org/Services/medium-to-markdown)

## The Cost Estimation

When thinking about what our limits are on giving away free services, we can approach the problem from two sides:

1. How much is the maximum number of requests going to cost?

1. How many requests can I get for $2/month?

On the [T3chFlicks](https://t3chflicks.org) site, we give users 100 free credits per week. At the time of of writing, we have 100 registered users. If we assume all of our users use all of their credits each week for a month on the Medium to Markdown service, then…

    Number of requests/month = (100 credits/week * 100 users * 4.35 weeks/month) = 43,500 Requests / Month

That’s a small number of requests, but will it incur a small AWS cost?

The total cost of the service is the sum of the individual component costs:

    Total Cost = (ALB cost) + (Lambda cost) + (SQS cost) + (S3 cost) + (CloudFront cost)

These costs are dependent on the amount of data transferred. Apparently, there is an optimum length for a [Medium article](https://www.lean-labs.com/blog/the-ideal-length-for-business-blog-posts-when-less-is-more#:~:text=Here's%20what%20recent%20studies%20have,between%202%2C350%20and%202%2C500%20words) ~ 1,600 words. At 4.79 characters per word on average in UTF-8 means:

    Size of Article = 1600*4.79*1byte = 7,664 bytes ~7.7KB

An example [T3chFlicks article](https://t3chflicks.medium.com/how-to-use-amplify-auth-in-nuxt-js-4dbf07da7033) has a size of **5.39KB**, so this seems legit.

    Data transfer/ month = (number of requests / month) * (size of response)
    *Data transfer / month = 7.7 KB * 4350 Requests per Month = 33,495 KB ~ 33.5MB

### Load Balancing cost

The API is created by an ALB. The cost is broken down into:

* $0.0252 per ALB-hour (or partial hour)

* $0.008 per Load balancing capacity unit - LCU hour (or partial hour)

LCUs have four usage dimensions and you are charged based on the highest dimension:

1. Number of newly established connections per second (25/sec)

1. Number of active connections per minute (3,000/min)

1. The number of bytes processed for requests and responses (1 GB /hour on EC2, and 0.4GB/hour Lambda)

1. Number of Rule evaluations (1,000/sec)

Determining this cost is quite difficult, so we made use of the calculator on the [ALB page](https://aws.amazon.com/elasticloadbalancing/pricing/). However, with our estimates for usage of this service, the cost seems to be negligible.

The size of the request is tiny:

`Processed bytes = (33Bytes request + 33Bytes response) * 4350 requests = 287,100B = 287KB = 0.287MB = 0.0003GB`

![](https://cdn-images-1.medium.com/max/3428/1*lESibyAQqPPnoZHCFoZxiw.png)

The estimated **$0.23** for LCU charges is very manageable for our goal of $2. Even at 26 million requests/month, the LCU charge only increases to $2.34.

A cheaper alternative given the predicted rate of requests is the [API Gateway](https://aws.amazon.com/api-gateway/) service. However, many services can share the same ALB, and since we can share this across many of our projects, so will the cost, meaning we can assume it to be zero.

    Total ALB cost = (ALB/month) + (LCU/month)
    Total ALB Cost = $0.23 +(730hours/month * $0.0252/hour) = $18.63

Once the traffic has used **~30 LCU**, then the cost of traffic will be equal to that of the unused ALB service.

### Lambda cost
> With AWS Lambda, you pay only for what you use. You are charged based on the number of requests for your functions and the duration, the time it takes for your code to execute — [source](https://aws.amazon.com/lambda/pricing/).

The are two different Lambdas in the service:

1. **API Lambda —** immediately returns a response of the result location

    ***197.5 ms on average @ 256 MB memory***

![](https://cdn-images-1.medium.com/max/2396/1*j6U896kNZpxNQlHnHi5B0A.png)

Only when getting into the millions of requests does this service begin to cost:

![](https://cdn-images-1.medium.com/max/2412/1*fnP1oUjL0Ty6cLSFsjqiEA.png)

2. **Processing Lambda —** performs the transformation of the article and uploads the result

This part of the service depends on the response from many third parties including Medium, YouTube, and Github. This means response times might vary wildly depending on the contents of the Medium blog post. A hard limit of 10 seconds was set on the Lambda runtime.

    650ms on average @ 256 MB memory for a standard length blog post

![](https://cdn-images-1.medium.com/max/2428/1*B92P4eoaszqYDL6DdG2A-A.png)
> # 😱 But what if users want to process huge articles 😱
> # ✅ Set a Lambda timeout to avoid long running times ✅

### Queue cost

This service does singular batches of items on the SQS queue, but could easily be extended to do larger batches. The pricing page shows that for fewer than a million requests, this service is free:

![](https://cdn-images-1.medium.com/max/3868/1*9HGDSv8Sm_6TGOuUc5f7pA.png)

We can therefore assume the SQS cost to be negligible as we do not expect a million requests per month.

### Storage cost

The result of the process is stored in an S3 bucket and users are sent a URL of that object.

At 4350 requests per month, ~135 requests per day, with a bucket lifecycle of one day, the maximum expected to be in the bucket at one point is:

    `200 articles, 7.7 KB each, 1,540KB = 1.5MB`

    `$0.023 per GB storage costs on S3 for the first 50TB`

    `1.5/1000 * 0.0023 = $0.00000345`

Again, this can be considered negligible, probably up until 10 million requests:

`7.7KB/1000/1000 * $0.0023/GB * 10,000,000R = $0.1771`

### CloudFront cost

CloudFront is used in this architecture as a layer around the S3 bucket. The costs for CloudFront origin requests (first time accessing) are free for S3 bucket origins and $0.085 for the first 10TB transferred to users, meaning this cost is negligible up until millions of requests.

### *Total Cost*

    For 4,350 requests
    Total Cost = (ALB cost) + (Lambda cost) + (SQS cost) + (S3 cost) + (CloudFront cost)

    Total = ( $18.396 + $0.23 )+ ($0.00 +$ 0.01) + ($0.00) + ($0.00 ) + ($0.00 )

    Total = $18.396 + $0.23 + $0.01

    Total = $18.636
    Total minus standard ALB charge = $0.24
> # 🙌 I think we can afford 24 cents per month 🙌

### Capping Usage

As we previously mentioned, the other way to look at this problem is:
> # *If we put a monthly cap of $2 on this service, how many requests could we support?*

For 435,000 requests **(100X more)**

* Lambda costs — $1.27

* Lambda costs — $0.45

* ALB costs — no change $0.23

* Storage costs — Negligible

* CloudFront costs — Negligible

`Costs = 1.27 + 0.45 + 0.23 = $1.95 ~ $2`

100 times more requests would mean 100 times more users:
> # *🌎 We’re happy with spending $2 on 10,000 people 🤗*

## The Real costs

### Cost Tagging

Tagging your resources makes it much easier to retrospectively understand costs, as the AWS billing console can effectively use these tags to split up the bill.
> # 😱 Resource costs are hard to pin down😱
> # ✅ Tag all resources and create a cost budget with project filters✅

### AWS Budgets

AWS offers [budgets](https://aws.amazon.com/getting-started/hands-on/control-your-costs-free-tier-budgets/) to help solve the problem of capping usage. The service allows you to filter service costs into a group and place alarms on monetary metrics such as expected monthly forecast. You can use these to trigger an email message.
> # 😱 But what if we suddenly get lots of users? 😱
> # ✅ Put a budget alarm on the service✅

We have done this for the [Medium-To-MarkDown](https://medium-to-markdown.t3chflicks.org/) service by tagging the service resources with a [user defined cost allocation tag](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/activating-tags.html): `Project` , and creating a budget which filters using the same tag.

A budget shows a detailed dashboard, which is rather empty at the moment:

![](https://cdn-images-1.medium.com/max/4928/1*kzOVl0O7IqPowwDarXS4-g.png)

## Other Considerations

### Rate Limiting

ALB does not allow for rate limiting. For that, you must add AWS WAF onto your API which costs $5/month + $1/month per million requests - quite expensive.

How bad would it be if somebody all spent their credits at once?

This could increase the LCU to a high level for a short period of time which could be bad but probably not awful.

### Service Status

It is good practice to monitor your service for errors. You can monitor how many users are receiving [4XX and 5XX responses](https://developer.att.com/video-optimizer/docs/best-practices/http-400-and-500-error-codes) from the ALB, and configure alarms which trigger email alerts.

**CI/CD**

We used AWS [CodePipeline](https://aws.amazon.com/codepipeline/) to orchestrate this entire service.

Alarms and a deployment pipeline with tests mean that we minimise the likelihood of updating this service with a breaking change.

### Conclusion

At T3chFlicks **we want to share**, this is why you’ll find that our projects – whether they’re a [Smart Buoy for ocean measurement](https://github.com/sk-t3ch/smart-buoy), or a [Software as a Service quickstart](https://github.com/sk-t3ch/AWS_Stripe-SaaS-quickstart) – are open sourced. This API is due to be followed by many other services and as long as we **don’t go broke**, we will continue. We’d love to hear from experienced developers / business owners on how they managed to run a successful SaaS, please reach out!

![](https://cdn-images-1.medium.com/max/2000/0*3YDT7Yy33equvSJ4.png)

## Thanks For Reading

I hope you have enjoyed this article. If you like the style, check out [T3chFlicks.org](https://t3chflicks.org/) for more tech focused educational content ([YouTube](https://www.youtube.com/channel/UC0eSD-tdiJMI5GQTkMmZ-6w), [Instagram](https://www.instagram.com/t3chflicks/), [Facebook](https://www.facebook.com/t3chflicks), [Twitter](https://twitter.com/t3chflicks), [Patreon](https://www.patreon.com/bePatron?u=14761480)).