Project Overview
In this project, I deployed my static portfolio website using Amazon S3, and I used CloudFront to serve it fast from edge locations. I also added HTTPS for my custom domain (jangtoor.com) using AWS Certificate Manager (ACM), and I used Route 53 as the authoritative DNS for my domain. I also implemented a visitor counter. The website is still just HTML/CSS/JavaScript, but the JavaScript calls a small serverless backend (Lambda + DynamoDB) to increment and fetch the latest visit count.
Architecture (How the request flows)
The system has three main flows:
•	Static website + DNS: Users resolve the domain via DNS and then load site content through CloudFront (with S3 as the origin).
•	Visitor counter: Browser JavaScript calls a Lambda Function URL, Lambda updates DynamoDB and returns the current count.
•	CI/CD deployment: On each push to GitHub, GitHub Actions deploys updated site files to S3 and optionally invalidates the CloudFront cache.

An architectural diagram can be included here showing the DNS lookup path, the CloudFront to S3 origin path, and the JavaScript to Lambda to DynamoDB path.

DNS and Routing
My domain is registered with Network Solutions (the registrar). I configured the domain’s nameservers to use the Route 53 nameservers for my hosted zone. This is called DNS delegation: it tells the internet to treat Route 53 as the authoritative source of DNS records for jangtoor.com. When a user visits https://jangtoor.com, the browser does not send the web request to Route 53. Instead, the browser (via a recursive DNS resolver) performs a DNS lookup. Route 53 replies with the DNS record that points the domain to my CloudFront distribution (typically A/AAAA alias records). After DNS resolution, the browser connects directly to CloudFront to fetch the website content.

HTTPS with ACM and CloudFront
CloudFront can serve HTTPS for a custom domain only if it has a certificate that matches that domain. I requested an ACM certificate for jangtoor.com (and www.jangtoor.com) and validated ownership using DNS validation.
With DNS validation, ACM provides one or more CNAME records containing unique tokens. By adding these CNAME records to my DNS (Route 53 hosted zone), I prove that I control the domain. ACM checks public DNS for those records, and once it finds them, the certificate is issued.
After the certificate was issued, I attached it to my CloudFront distribution. This allows users to access the site at https://jangtoor.com without certificate warnings. CloudFront also supports redirecting HTTP to HTTPS to enforce encrypted connections.

Static Content Delivery
The website files (HTML, CSS, JavaScript, and images) are stored in an S3 bucket. CloudFront is configured with the S3 bucket as its origin. When users request files, CloudFront returns cached content when available, otherwise it fetches the content from S3 and caches it at edge locations.
To prevent direct public access to the S3 bucket, I configured CloudFront with Origin Access Control (OAC). This ensures that the bucket can be read by CloudFront, while blocking direct public requests to S3.

Visitor Counter
The visitor counter runs as follows:
1.	The browser loads the webpage through CloudFront.
2.	A JavaScript function runs in the browser and sends an HTTPS request to the Lambda Function URL (this provides a public HTTP endpoint for Lambda).
3.	Lambda uses the AWS SDK to perform an atomic update in DynamoDB (UpdateItem) to increment the counter and read the latest value.
4.	Lambda returns JSON (for example, {"count": 11}).
5.	JavaScript updates the HTML element on the page to display the new count.
Because the website domain and the Lambda Function URL are different origins, I configured CORS on the Lambda Function URL to allow requests from my site’s domain. Lambda is allowed to access DynamoDB through its execution role (IAM). The role’s policy grants only the required actions (such as dynamodb:GetItem and dynamodb:UpdateItem) on the specific table.

CI/CD (GitHub Actions)
I stored the website source in a GitHub repository and set up a GitHub Actions workflow to automate deployments. On each push to the main branch, the workflow syncs the website files to the S3 bucket. To ensure updates appear immediately, the workflow can also create a CloudFront invalidation

Challenges and How I Fixed Them
Key issues I encountered and how I resolved them:
•	IAM permissions: Lambda initially failed with AccessDenied when calling DynamoDB. I fixed this by attaching the correct DynamoDB permissions to the Lambda execution role.
•	DNS records: The site did not route correctly until I created the correct A/AAAA alias records in Route 53 pointing my domain to CloudFront.
•	CORS: Browser requests to the Lambda Function URL were blocked until I configured CORS to allow my website domain.
•	Caching: Updates did not appear immediately due to CloudFront caching. I fixed this by creating CloudFront invalidations as part of deployment.

Overall, this project helped me connect a lot of separate AWS services into one real working system: DNS (Route 53), HTTPS (ACM), caching/global delivery (CloudFront), static hosting (S3), and a serverless backend (Lambda + DynamoDB).
