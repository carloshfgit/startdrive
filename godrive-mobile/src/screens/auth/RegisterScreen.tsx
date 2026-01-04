import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';
import { useNavigation } from '@react-navigation/native';

export const RegisterScreen = () => {
  const navigation = useNavigation();
  return (
    <View style={styles.container}>
      <Text>Tela de Cadastro (Em construção)</Text>
      <Button title="Voltar" onPress={() => navigation.goBack()} />
    </View>
  );
};
const styles = StyleSheet.create({ container: { flex: 1, justifyContent: 'center', alignItems: 'center' } });