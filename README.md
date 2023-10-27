# Challenge
**Ops | Back-end Python Developer**

## Instructions
**1. Follow README-DevEnv.md to set up a development environment for the exercise.**
   -  Able to run locally, debug, unit-test. ✓
   -  Able to smoke-test and performance test. ✓

**2. Do the following tasks:**
   -  Enhance product service. ✓
     - Add an Update RPC call
     - Create a paginated list RPC call
     - Add exception to the methods 
   -  Delete product RPC call. ✓
   -  Wire into smoketest.sh. ✓
   -  (Bonus) Wire into perf-test. ✓
   -  (Bonus) Wire unit-test for this method. ✓
   -  Enhance order service. ✓
     - Add a Delete RPC call
     - Add caching to the get method
     - Add a paginated list RPC call
     - Add exception to the methods 
   -  List orders RPC call.  ✓
   -  Wire into smoketest.sh. ✓
   -  (Bonus) Wire into perf-test. ✓
   -  (Bonus) Wire unit-test for this method. ✓
   -  Execute performance test. ✓

## Questions and Answers

### Question 1: Why is performance degrading as the test run longer?
- **Answer:** 
   - The performance degradation during extended test runs is primarily due to the services' practices of loading substantial amounts of data without implementing essential optimizations such as pagination and caching. 
     - These two crucial elements are vital for efficient data retrieval and management, reducing the strain on resources and improving overall service responsiveness.
        - Perfomance Before: 
       ![perf test before.png](perf%20test%20before.png)
### Question 2: How do you fix it?
 - **Answer:** 
      - I addressed the performance degradation issue by implementing the following key solutions:
        - Added pagination to methods that load significant amounts of data. This ensures that data is retrieved in manageable chunks, reducing memory consumption and enhancing efficiency.
        - Introduced a cache to the methods responsible for querying data from both PostgreSQL and Redis. Caching minimizes the need for repetitive data retrieval, 
        resulting in faster response times and reduced resource usage. These optimizations collectively improved service performance during prolonged test runs.
           - Perfomance After: 
          ![perf test after.png](perf%20test%20after.png)
   - ✓ (Bonus): Fixed it. ✓
