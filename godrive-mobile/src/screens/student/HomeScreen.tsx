// Arquivo: src/screens/student/HomeScreen.tsx

import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, Alert, Dimensions } from 'react-native';
import MapView, { Marker, PROVIDER_GOOGLE } from 'react-native-maps';
import * as Location from 'expo-location';
import { useAuthStore } from '../../stores/useAuthStore';

export const HomeScreen = () => {
  const { user, signOut } = useAuthStore();
  
  // Estado para guardar a localização do usuário
  const [location, setLocation] = useState<Location.LocationObject | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      // 1. Pedir Permissão
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setErrorMsg('Permissão de localização negada. O app precisa do GPS para encontrar instrutores.');
        setLoading(false);
        return;
      }

      // 2. Pegar Localização Atual
      try {
        let currentLocation = await Location.getCurrentPositionAsync({});
        setLocation(currentLocation);
      } catch (error) {
        Alert.alert('Erro', 'Não foi possível obter sua localização.');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text>Buscando sua localização...</Text>
      </View>
    );
  }

  if (errorMsg) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.errorText}>{errorMsg}</Text>
        <Text style={styles.link} onPress={signOut}>Sair</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {location && (
        <MapView
          style={styles.map}
          // No Android usa Google Maps, no iOS usa Apple Maps nativo (ou Google se configurado)
          provider={undefined} 
          initialRegion={{
            latitude: location.coords.latitude,
            longitude: location.coords.longitude,
            latitudeDelta: 0.015, // Zoom
            longitudeDelta: 0.015,
          }}
          showsUserLocation={true} // Mostra a bolinha azul do usuário
          showsMyLocationButton={true} // Botão para recentralizar
        >
           {/* Aqui virão os Markers dos Instrutores depois */}
        </MapView>
      )}
      
      {/* Overlay simples com o nome do usuário (apenas para teste) */}
      <View style={styles.overlay}>
        <Text style={styles.welcomeText}>Olá, {user?.full_name?.split(' ')[0]}</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  map: {
    width: Dimensions.get('window').width,
    height: Dimensions.get('window').height,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  errorText: {
    color: 'red',
    textAlign: 'center',
    marginBottom: 20,
    paddingHorizontal: 20,
  },
  overlay: {
    position: 'absolute',
    top: 50,
    left: 20,
    backgroundColor: 'white',
    padding: 10,
    borderRadius: 8,
    elevation: 5, // Sombra Android
    shadowColor: '#000', // Sombra iOS
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  welcomeText: {
    fontWeight: 'bold',
    color: '#333',
  },
  link: {
    color: '#007AFF',
    marginTop: 10,
  }
});