import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, Alert, Dimensions, Image } from 'react-native';
import MapView, { Marker, Callout } from 'react-native-maps'; // Adicionado Callout
import * as Location from 'expo-location';
import { useAuthStore } from '../../stores/useAuthStore';
import { searchInstructors } from '@/services/instructorService'; // Importe o serviço
import { Instructor } from '@/types/instructor'; // Importe o tipo

export const HomeScreen = () => {
  const { user, signOut } = useAuthStore();
  
  const [location, setLocation] = useState<Location.LocationObject | null>(null);
  const [instructors, setInstructors] = useState<Instructor[]>([]); // Estado dos instrutores
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      // 1. Permissão e Localização
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setErrorMsg('Permissão negada.');
        setLoading(false);
        return;
      }

      try {
        const currentLocation = await Location.getCurrentPositionAsync({});
        setLocation(currentLocation);

        // 2. Busca Instrutores Próximos (Assim que tiver a localização)
        const foundInstructors = await searchInstructors({
            latitude: currentLocation.coords.latitude,
            longitude: currentLocation.coords.longitude,
            radius: 15 // Raio de 15km
        });
        setInstructors(foundInstructors);

      } catch (error) {
        // Não bloqueia o app, mas avisa (ou falha silenciosamente)
        console.log('Erro ao carregar instrutores');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <ActivityIndicator style={styles.loading} size="large" color="#007AFF" />;
  if (errorMsg) return <Text style={styles.error}>{errorMsg}</Text>;

  return (
    <View style={styles.container}>
      {location && (
        <MapView
          style={styles.map}
          initialRegion={{
            latitude: location.coords.latitude,
            longitude: location.coords.longitude,
            latitudeDelta: 0.04, // Zoom um pouco mais aberto para ver instrutores
            longitudeDelta: 0.04,
          }}
          showsUserLocation={true}
          showsMyLocationButton={true}
        >
           {/* Renderiza os Instrutores encontrados */}
           {instructors.map((inst) => (
             <Marker
               key={inst.id}
               coordinate={{ latitude: inst.latitude, longitude: inst.longitude }}
               title={inst.full_name}
               description={`${inst.car_model} - R$ ${inst.hourly_rate}/h`}
             >
                {/* Opcional: Customizar o ícone do marcador */}
                <View style={styles.markerContainer}>
                    <Text style={styles.markerText}>🚗</Text> 
                </View>

                {/* Balãozinho ao clicar */}
                <Callout>
                    <View style={styles.callout}>
                        <Text style={styles.calloutTitle}>{inst.full_name}</Text>
                        <Text>⭐ {inst.rating} • {inst.car_model}</Text>
                        <Text style={styles.price}>R$ {inst.hourly_rate},00 / aula</Text>
                    </View>
                </Callout>
             </Marker>
           ))}
        </MapView>
      )}
      
      <View style={styles.overlay}>
        <Text style={styles.welcomeText}>Olá, {user?.full_name?.split(' ')[0]}</Text>
        <Text style={styles.subText}>{instructors.length} instrutores online</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  map: { width: Dimensions.get('window').width, height: Dimensions.get('window').height },
  loading: { flex: 1, justifyContent: 'center' },
  error: { flex: 1, textAlign: 'center', marginTop: 50 },
  overlay: {
    position: 'absolute', top: 50, left: 20,
    backgroundColor: 'white', padding: 12, borderRadius: 10,
    elevation: 5, shadowOpacity: 0.25, shadowRadius: 3.84,
  },
  welcomeText: { fontWeight: 'bold', fontSize: 16 },
  subText: { color: '#666', fontSize: 12 },
  
  // Estilos do Marker e Callout
  markerContainer: {
      backgroundColor: 'white', padding: 5, borderRadius: 20, borderWidth: 1, borderColor: '#007AFF'
  },
  markerText: { fontSize: 20 },
  callout: { width: 150, padding: 5 },
  calloutTitle: { fontWeight: 'bold', marginBottom: 5 },
  price: { color: 'green', fontWeight: 'bold', marginTop: 5 }
});