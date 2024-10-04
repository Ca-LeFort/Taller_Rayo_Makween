function confirmarDelete(id) {
  Swal.fire({
    title: "¿Estás seguro de eliminar?",
    text: "¡Después de eliminar, no se puede revertir!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Sí",
    cancelButtonText: "No"
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title: "¡Eliminado!",
        text: "¡El mecánico ha sido eliminado de forma correctamente!",
        icon: "success"
      }).then(function(){
        window.location.href = "mecanicodelete/" + id + "/"
      }) 
    }
  });
}

function test() {
  Swal.fire({
    title: "¿Estás seguro de eliminar?",
    text: "¡Después de eliminar, no se puede revertir!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Sí",
    cancelButtonText: "No"
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title: "Deleted!",
        text: "Your file has been deleted.",
        icon: "success"
      });
    }
  });
}