export default {
  t3chflicksRootDomain: `https://${process.env.t3chflicksRootDomain}`,
  serviceRootDomain: `https://${process.env.serviceRootDomain}`,
  serviceApiDomain: `https://${process.env.serviceApiDomain}`,
  name: 'Medium To MarkDown',
  slug: 'medium-to-markdown',
  openRepository: 'https://github.com/sk-t3ch/medium-to-markdown',
  endpoints: [
    {
      path: '/convert',
      method: 'POST',
      credits: 1
    }
  ],
  description: 'Convert a Medium post to MarkDown',
  examples: [
    {
      link: 'https://t3chflicks.org/Projects/catboost-quickstart',
      title: 'T3chFlicks Blogs'
    },
    {
      link: 'https://github.com/sk-t3ch/AWS_Stripe-SaaS-quickstart/blob/master/blog_post.md',
      title: 'Github Blogs'
    }
  ],
  features: [
    {
      name: 'Different heading and text styles',
      items: []
    },
    {
      name: 'Image embeds',
      items: []
    },
    {
      name: 'Youtube Video embeds',
      items: []
    },
    {
      name: 'Gist Code Embeds',
      items: []
    }
  ]
}
