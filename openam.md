# ForgeRock OpenAM

https://idmdude.com/2014/02/09/how-to-configure-openam-signing-keys/
http://100bytes.com/tutorials/java/keytool

## Managing the keystore

	# keytool -genkeypair -alias userregkeypair -keypass almafa -keystore keystore -storepass almafa137 -storetype JCEKS -keyalg RSA -keysize 2048 -sigalg SHA256withRSA -dname "cn=dobos,ou=compare,o=elte,l=budapest,s=bp,c=hu" -v
	
	# keytool -genseckey -keystore keystore -storepass almafa137 -storetype JCEKS -alias userregseckey -keypass almafa -keyalg aes -keysize 256 -v
	
	# keytool -keystore keystore -storetype JCEKS -list -storepass almafa137
	
