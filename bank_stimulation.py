import random                #importing required libraries
import simpy
NEW_CUSTOMERS =5             #no of customers that are going to enter the bank in the stimulation
INTERVAL_CUSTOMERS =10.0     #Patience min and max level
MIN_PATIENCE=1
MAX_PATIENCE=3
 
def customer(env,name,counter,time_in_bank):   #a function to generate a customer                                    
  arrive=env.now                               #arrival time of the customer
  print('%7.4f: %s Arrived' % (arrive, name))  #displaying arrival time
  with counter.request() as req:               #generating request for acquiring counter
      patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)#generating random patience value for customer
                                                           # Wait for the counter or abort at the end of our tether
      results = yield req | env.timeout(patience)           #result is either acquiring the counter or patience run out
      
      
      
      wait = env.now - arrive          #waiting time for customer is calculated
      if req in results:               #if counter is available 
          # We got to the counter
          print('%7.4f: %s Waited %6.3f' % (env.now, name, wait)) #print wait time
 
          tib = random.expovariate(1.0 / time_in_bank)            #generating the time it took to to complete the request
 
          yield env.timeout(tib)
          print('%7.4f: %s Finished' % (env.now, name))                #getting and printing TIB
 
      else:
        print('%7.4f: %s RENEGED after %6.3f' % (env.now, name, wait))       #print the time after which customer left or patience ran out
def source(env, number, interval, counter):                   #function to generate multiple customers for the stimulation
    """Source generates customers randomly"""
    for i in range(number):
        c = customer(env, 'Customer%02d' % i, counter, time_in_bank=12.0)
        env.process(c)                     #each customer is made into a process  
 
        t = random.expovariate(1.0 / interval) #with a random but sequential time
        yield env.timeout(t)
 
 #Setup and start the simulation
print('Bank renege') #title  of stimulation
env = simpy.Environment() #making environment
# Start processes and run
counter = simpy.Resource(env, capacity=1) #giving limit of resource for environment here it is counter
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()   #running stimulation
