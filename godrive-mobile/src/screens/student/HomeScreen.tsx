import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { useAuthStore } from '../../stores/useAuthStore';

export const HomeScreen = () => {
  const signOut = useAuthStore(state => state.signOut);
  const user = useAuthStore(state => state.user);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Olá, {user?.full_name}</Text>
      <Text>Mapa do Aluno (Em breve)</Text>
      <Button title="Sair" onPress={signOut} />
    </View>
  );
};
const styles = StyleSheet.create({ 
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 20, fontWeight: 'bold', marginBottom: 20 }
});