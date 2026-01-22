import React, { useState } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  ActivityIndicator, 
  KeyboardAvoidingView, 
  Platform,
  TouchableWithoutFeedback,
  Keyboard
} from 'react-native';
import { useAuthStore } from '../../stores/useAuthStore';
import { useNavigation } from '@react-navigation/native';
import { LogIn } from 'lucide-react-native';

export const LoginScreen = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigation = useNavigation<any>();
  
  const { signIn, isLoading, error } = useAuthStore();

  const handleLogin = async () => {
    await signIn({ username: email, password });
  };

  return (
    <KeyboardAvoidingView 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      className="flex-1 bg-background"
    >
      <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
        <View className="flex-1 justify-center px-8">
          
          {/* Cabeçalho / Logo */}
          <View className="items-center mb-12">
            <View className="bg-indigo-100 p-4 rounded-full mb-4">
              <LogIn color="#4F46E5" size={32} />
            </View>
            <Text className="text-4xl font-bold text-slate-900">UDrive</Text>
            <Text className="text-slate-500 mt-2 text-center">
              Acesse sua conta para continuar
            </Text>
          </View>

          {/* Formulário */}
          <View className="space-y-4">
            <View>
              <Text className="text-slate-700 font-medium mb-2 ml-1">Email</Text>
              <TextInput 
                className="bg-white border border-slate-200 rounded-xl p-4 text-slate-800"
                placeholder="exemplo@email.com"
                placeholderTextColor="#94A3B8"
                autoCapitalize="none"
                keyboardType="email-address"
                value={email}
                onChangeText={setEmail}
              />
            </View>

            <View>
              <Text className="text-slate-700 font-medium mb-2 ml-1">Senha</Text>
              <TextInput 
                className="bg-white border border-slate-200 rounded-xl p-4 text-slate-800"
                placeholder="••••••••"
                placeholderTextColor="#94A3B8"
                secureTextEntry
                value={password}
                onChangeText={setPassword}
              />
            </View>
            
            {/* Mensagem de Erro */}
            {error && (
              <View className="bg-red-50 p-3 rounded-lg border border-red-100">
                <Text className="text-red-500 text-center text-sm">{error}</Text>
              </View>
            )}

            {/* Botão de Ação */}
            <TouchableOpacity 
              className={`bg-primary rounded-xl py-4 mt-4 shadow-lg shadow-indigo-500/30 ${isLoading ? 'opacity-70' : ''}`}
              onPress={handleLogin}
              disabled={isLoading}
            >
              {isLoading ? (
                <ActivityIndicator color="#FFF" />
              ) : (
                <Text className="text-white text-center font-bold text-lg">Entrar</Text>
              )}
            </TouchableOpacity>
          </View>

          {/* Rodapé */}
          <View className="flex-row justify-center mt-8">
            <Text className="text-slate-500">Não tem uma conta? </Text>
            <TouchableOpacity onPress={() => navigation.navigate('Register')}>
              <Text className="text-primary font-bold">Cadastre-se</Text>
            </TouchableOpacity>
          </View>

        </View>
      </TouchableWithoutFeedback>
    </KeyboardAvoidingView>
  );
};