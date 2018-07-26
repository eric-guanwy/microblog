from redis import Redis
import rq
from rq import get_current_job
import time

def example(seconds):
    print('starting task')
    for i in range(seconds):
        print(i)
        time.sleep(1)
    print('task completed!')
        
        

def test(t):
    job = get_current_job()
    print('starting task')
    for i in range(t):
        job.meta['progress'] = 100.0*i/t
        job.save_meta()
        print(i)
        time.sleep(1)
    job.meta['progress'] = 100
    job.save_meta()
    print('task completed!')

if __name__ == '__main__':
    queue = rq.Queue('microblog-tasks', connection=Redis.from_url('redis://'))
    job = queue.enqueue('app.tasks.example',23)
    print(rq.job.Job.fetch(job.get_id(),connection=Redis.from_url('redis://')))