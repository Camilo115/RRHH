package cl.proyecto.recursos_humanos_autenticacion_service.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import cl.proyecto.recursos_humanos_autenticacion_service.model.Usuario;

public interface UsuarioRepository extends JpaRepository<Usuario, Integer> {
 
    Optional<Usuario> findByCorreo(String correo);
}
