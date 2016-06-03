# ForgeRock OpenAM

https://idmdude.com/2014/02/09/how-to-configure-openam-signing-keys/
http://100bytes.com/tutorials/java/keytool
http://blogs.forgerock.org/petermajor/2010/09/how-to-change-the-default-signing-key-for-federation/

## Managing the keystore

Default keystore pass is changeit

	# keytool -genkeypair -alias userregkeypair -keypass almafa -keystore keystore.jceks -storepass changeit -storetype JCEKS -keyalg RSA -keysize 2048 -sigalg SHA256withRSA -dname "cn=dobos,ou=compare,o=elte,l=budapest,s=bp,c=hu" -v
	
	# keytool -genseckey -keystore keystore.jceks -storepass changeit -storetype JCEKS -alias userregseckey -keypass almafa -keyalg aes -keysize 256 -v
	
	# keytool -keystore keystore -storetype JCEKS -list -storepass almafa137
	

Then need to change keystore type under Configure/Server Defaults/Security, use JCEKS

## Setting up email server

Configure/Global Services/Email Service

## Setting up user self-service

