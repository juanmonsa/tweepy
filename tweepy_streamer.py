from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credential

# La clase StremListener contiene métodos que pueden ser utilizados directamente
class StdOutListener(StreamListener):

    # El método on_data toma como entrada un parámetro data, es un método de costo.
    # on_data toma los datos que están siendo streamed in desde el listener
    def on_data(self, data):
        print(data)
        return True

    # El método on_error ocurre cuando se produce algún error
    # Cuando un error suceda el método on_error será triggeado y el estado del error será impreso
    def on_error(self, status):
        print(status)


if __name__ == "__main__":
    # Listener es un objeto creado a partir de la clase anterior
    listener = StdOutListener()

    # auth es un objeto de autenticación que hereda de la clase OAuthHandler
    auth = OAuthHandler(twitter_credential.CONSUMER_KEY, twitter_credential.CONSUMER_SECRET)
    auth.set_access_token(twitter_credential.ACCESS_TOKEN, twitter_credential.ACCESS_TOKEN_SECRET)

    # El objeto stream se conectará usando las credenciales de auth y manejará los datos y errores según lo definido en la clase StdOutListener
    stream = Stream(auth, listener)
    stream.filter(track=['donald trump', 'hillary clinton'])


# CTRL+ALT+N : Imprimirá en consola el stream de Tweets que están siendo capturados por el listener 