
# ALB Reutilizable

Este proyecto crea los siguientes recursos dentro de una región de AWS:

* 1 Application Load Balancer
* Https listener
* Http listener usando certificado ACM existente, redireccionado a https
* 2 security groups (alb y target groups)
* Funcion AWS Lambda para realizar logout cuand la ruta es /logout (cuando se usa autenticación)
* 1 registro alias para el alb dns en la zona hosteada existente
* 1 regla de respuesta fija "Hello World" cuando se navega al home del balanceador
* Parametros en parameter store:
    * security group id para usar en target groups
    * security group id del balanceador
    * arn del balanceador
    * arn del listener https

La idea de este proyecto es contar con un balanceador para diferentes proyectos futuros. Solo agregndo nuevos target groups y las reglas de balanceo.



![application load balancer](/alb.jpg)

El codigo de la infra está en [`load_balancer_stack.py`](load_balancer/load_balancer_stack.py)


## Instrucciones para despliegue


Clonar y crear un ambiente virtual python para el proyecto

```zsh
git clone https://github.com/ensamblador/reusable-alb.git
cd reusable-alb
python3 -m venv .venv
```

En linux o macos el ambiente se activa así:

```zsh
source .venv/bin/activate
```

en windows

```cmd
% .venv\Scripts\activate.bat
```

Una vez activado instalamos las dependencias
```zsh
pip install -r requirements.txt
```

en este punto ya se puede desplegar:

```zsh
cdk deploy
```

y para eliminar:

```zsh
cdk destroy
```


## Otros comandos útiles

 * `cdk synth`       crea un template de cloudformation con los recursos de este proyecto
 * `cdk diff`        compara el stack desplegado con el nuevo estado local

Enjoy!
