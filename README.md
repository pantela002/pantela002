# Hi, I am Uroš 👋

```text
.....:-----===+***#################*+*%%  
.....:::-+=-=*++++++**************+-=+*%  
......:=+-:-@@+##++++++++++++++++++-:-=+     uros@github
......::-=:=#++%**@*=*+*+*+#*+#**%@-:::-     -----------
.......:**:======+==*++++++**=**+*#=.:.-     OS:        Windows 11 + WSL Ubuntu
.......-=::++==+=+=%*++=++=========-.:::     Uni:       University of Belgrade, EE
.....::.. -+++++++#@*#***%+++=+====-=+++     Now:       Backend SWE Intern @ Nextesy
 ...-==:  -++++***%@#%###@#+*+++===-+:--     Prev:      Tenstorrent, Microsoft
  .-=-:...===##::+#%%%%%%****++=+==:. .:     Languages: Python, C++, Java, TypeScript
  -=-.....-==%%+=+%@@@@@@%-.=**====:  .=     Backend:   FastAPI, Django, Postgres, Redis
.:=:..:...-==##%%%%@@@@@@@#+*#%===-..  :     ML:        PyTorch, JAX/Flax, HuggingFace
.--  .:...-=-=%%%%%%@%@%%%%%%%*-==:.. .=     Interests: distributed systems, LLM infra
:-.. ::.. :+=.+@@%%%%%%%%%%%%#===-.... =     Web:       pantelicu.space
::......-=+*+-:+#%@%%%%%@@%%+:=+=......:  
     -#%@@@#*====+*%%%%##*+=-=++: ... :=  
    *@@@%%@#*#%+=++++++++====**##+-  .:=  
...#@%%%%%%***@@*++++++++=++**#@@@@*::-=  
=-#@%%%%%%*+**#**%#**+***%@#**#@%%%@%--=  
+#@%%%%###+*#*+**%%%%%%@+##**+#%%%%%%*-=  
+#%%%%%*#*+#*#%%*+*%%#*+++*@#+*%%%%%%%++  
```

Backend and ML infrastructure engineer from Belgrade. I like systems where many
things run at once: job schedulers, agent orchestration, LLM inference.

### Things I built

**AI Agent Orchestrator**: Python CLI and daemon that runs several Claude Code
agents in parallel, each in its own git worktree and tmux session, with a shared
task queue, per-task locking and crash recovery.

**Cloud-Native Distributed Inference Platform**: Kubernetes-style job scheduler
for CNN inference. Worker pools with dynamic scaling, DAG dependencies, fault
recovery and a live dashboard over WebSockets.

**Daily AI Chat Game**: full-stack web game (Next.js, Supabase, Stripe) where all
players face the same AI character each day and an LLM scores every conversation
on confidence, creativity and smoothness.

**Open source**: tensor-parallel inference for LLaMA 3.1 8B in JAX/Flax on
Tenstorrent hardware, contributed to
[TT-XLA](https://github.com/tenstorrent/tt-xla).

### Find me

[pantelicu.space](https://pantelicu.space) | pantelicu02@gmail.com
