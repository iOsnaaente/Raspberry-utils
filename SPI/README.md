
### Habilitando o SPI no Raspberry pi: 

Para verificar se o SPI esta ativo, pode-se fazer via terminal `lsmod | grep spi` e a saída deverá ser algo como:
```
spidev                 20480  0
spi_bcm2835            20480  0
```

Se a saída não for essa, pode ser que o SPI esteja desativo. Para ativar o SPI, pode-se editar diretamente no arquivo de configurações:
```
& sudo nano /boot/config.txt
```

E garanta que a linha `dtparam=spi=on` esteja presente. Se a linha for adicionada, deve-se fazer o reboot do sistema.
```
sudo reboot 
```

Outra maneira de ativar o SPI é através do raspi-config:
```
sudo raspi-config 
```

Na tela que abrir vá em Interface -> SPI -> Enable ? Sim. Faça o reboot após o processo.


### Instalação do SPIDEV para python 

Para se utilizar o SPI deve-se instalar o spidev via:
```
sudo apt-get update
sudo apt-get install python3-pip    
sudo pip3 install spidev
```

Para mais informações sobre o SPIDEV pode-se ver a documentação em:
https://www.sigmdel.ca/michel/ha/rpi/dnld/draft_spidev_doc.pdf (Acesso em: 02/02/2024)


### Utilizando o SPI via Python 

Para utilizar a biblioteca Python spidev basta fazer
```
spi = spidev.SpiDev()
spi.open( Canal, Dispositivo )
```

Onde o canal é o canal padrão da Raspberry pi definida pela numeração das GPIO e o Dispositivo é o chip select usado. Para testar as disponíveis pode-se fazer via terminal `ls /dev/spi*` e devera sair uma lista semelhante a:
```
/dev/spidev0.0  
/dev/spidev0.1
```
Onde o primeiro valor após spidev é o canal e o segundo o dispositivo disponível 

Para transmitir alguma coisa via SPI pode-se utilizar `ret = spi.xfer( bytearray )`. Como o SPI é full duplex, sempre que se envia algo, se recebe algo em troca que ficara armazenado no buffer SPI. Um exemplo de leitura de um registrador de 16 bits pode ser visto em:
```
ADDR = ADDR.to_bytes( 2, addr | (RW << 15), byteorder='big' ) 
ret = spi.xfer( [ ADDR, 0x00, 0x00 ] )    
```

Para configurar a velocidade do barramento SPI pode-se fazer `spi.max_speed_hz = NUM_BPS` 

### Visualizando o SPI 

Para visualizar a saída SPI pode-se utilizar a ferramenta disponível no Raspberry chamado `pigpio` e `piscope`. Para instalar as duas, pode-se fazer via terminal: 
```
# Instalando o pigpio
sudo apt install pigpio

# Instalando o piscope
wget abyz.me.uk/rpi/pigpio/piscope.tar   
tar xvf piscope.tar
cd piscope/
make hf
make install 
``` 

Com isso, ambas ferramentas já estarão instaladas. Para executar basta fazer:
```
sudo pigpio
sudo piscope 
```

Após executado, uma janela se abrira, mostrando o estado de cada pino da Raspberry, podendo se visualizar as transações via SPI. Para visualizar melhor, pode-se ajustar os parametros do piscope de acordo com a necessidade, ajustando o tempo de janela e disparo do trigger.