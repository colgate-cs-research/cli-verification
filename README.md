## cli-verification

### Setting up
1. Make sure you have a clone of pict in your clone of this repo - `git clone https://github.com/microsoft/pict.git`  
2. Make sure to start/restart the frr container by running `min_frr_config.py`.  
3. Then make sure that expect is installed in the container by running `docker exec -it myfrr bash` and then `apk add expect`.  

### Usage
1. Add your desired command templates to `config_templates`.  
2. Run `generate_expect.py`. This will generate a `config_writer` expect file.  
3. Make sure the Docker container is set up.  
4. Copy the `config_writer` file to the frr docker container by running: `docker cp config_writer myfrr:/`  
5. Run `docker exec -it myfrr bash` to access the frr container.   
6. Run `expect config_writer`, wait for it to finish.   
7. Copy the file's over by running `docker cp myfrr:/tests.log .`  
8. Run `check_logs.py` to check and flag tests.   


