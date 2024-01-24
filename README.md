# BRICK

[`BRIG`]()-like interactive data visualization for bacterial whole genome annotation and comparison.

## Overview

`BRICK` is under active development. Feel free to check out a demonstration of the application stack at: [https://brick.ink](https://brick.ink). Please note there is currently no guarantee for data persistence or backwards compatabiltity until major version release. 


## Stack deployment

`BRICK` is fairly easy to deploy on your local machine (desktop/laptop) if you have `Docker` installed. You can run a preconfigured local production stack of the latest release like this:

```bash
# Clone latest release on main and enter repository
git clone https://github.com/esteinig/brick && cd brick

# -d for detached mode
docker compose --profile prod up 

# Application available in your browser at: http://localhost:5473/ 
```

The production stack comes with a database cleaner that removes sessions and session working directories in the `work` volume. 

```bash
docker compose --profile prod --profile server up 
```

Default interval (every day) and expiration time (7 days) can be changed in `docker-compose.yml`.

```yml
command: brick utils clean --expire-days 3 --day-of-week "*" --time-of-day '04:00' --log /tmp/brick-cleaner.log
```

Some minor unit tests can be run with the `tests` service:

```bash
docker compose run tests
```

To update to the latest stable release version:

```bash
git pull # update
docker compose --profile prod up --rebuild 
```

## Dependencies

`BRICK` would not be possible without the amazing work of bioinformaticians and researchers who make their software available open-source. 
If you use their tools in the visualization, please cite the following publications:

> [Altschul et al. (1990)](https://pubmed.ncbi.nlm.nih.gov/2231712/) - Basic local alignment search tool - Journal of Molecular Biology

> [Camargo et al. (2023)](https://www.nature.com/articles/s41587-023-01953-y) - Identification of mobile genetic elements with geNomad - Nature Biotechnology

> [Sherry et al. (2023)](https://www.nature.com/articles/s41467-022-35713-4) - An ISO-certified genomics workflow for identification and surveillance of antimicrobial resistance (abritAMR) - Nature Communications

If you would like to acknowledge the authors of the original visualization, please cite:

> [Alikhan et al. (2011)](https://bmcgenomics.biomedcentral.com/articles/10.1186/1471-2164-12-402) - BLAST Ring Image Generator (BRIG): simple prokaryote genome comparisons - BMC Genomics

Similarly, the stack would not be possible without the following amazing tools:

* [Svelte/Sveltekit](https://kit.svelte.dev/)
* [Skeleton UI](https://www.skeleton.dev/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Celery](https://docs.celeryq.dev/en/stable/)
* [Redis](https://github.com/redis/redis)
* [MongoDB](https://www.mongodb.com/)

## Etymology

I thought it would be funny because the visualization is not very brick-like. **BR**IG-like **I**nteractive **C**ircular **K**nowledgabase is a bit of a stretch though...

## Contributors

Eike Steinig - @esteinig