# Alfred para Chalice

![Alfred](https://upload.wikimedia.org/wikipedia/commons/8/80/Alfred_Thaddeus_Crane_Pennyworth.jpg)

Alfred Thaddeus Crane Pennyworth é um personagem fictício da DC Comics. Ele é mordomo e tutor do bilionário Bruce Wayne.

Alfred tem sua origem muitas vezes envolta em mistério e pouco se fala de suas atividades antes de ele se tornar mordomo da rica e tradicional família Wayne. Em algumas mini-series e edições avulsas das HQs fala-se de sua distante ligação com a Scotland Yard onde ele teria trabalhado como um de seus agentes mais discretos.

Sabe-se ainda de um passado como ator competente, tendo essa experiência na dramaturgia se provado útil em diversas ocasiões. Como, por exemplo, tendo ensinado ao Bruce, ainda jovem, como modificar sua voz para imitar as vozes de outras pessoas. Algo que se provou muito útil na criação da persona do Homem-Morcego.

Demonstra também muitas outras habilidades úteis, como conhecimentos médicos básicos, por exemplo. Contudo, fica-se com a impressão que nem Bruce Wayne conhece totalmente esse passado de seu mordomo. Muitas vezes, as palavras de Alfred são sugestões quase que subliminares que ajudam o "cruzado mascarado" na solução de enigmas complexos de crimes. Mesmo assim, Alfred, várias vezes, faz o papel de ingênuo.


## Cache

Para utilizar a classe de cache do Alfred, primeiramente deve adicionar o walrus (https://walrus.readthedocs.io/en/latest/api.html) no seu requirements, recomendamos versões maiores que a **0.8.2**

```requirements
walrus==X.X.X
```

Após adicionar o walrus no projeto, você deve adicionar a sua conexação com o redis nas variáveis de ambiente do projeto.

```
ALFRED_REDIS_HOST=sua-conexao-com-redis
```
