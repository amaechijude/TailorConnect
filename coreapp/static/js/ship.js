function validateDigit(event) {
    const key = event.key;
    const allowedKeys = [
      '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+',
      'Backspace', 'Tab', 'Delete', 'Enter', 'ArrowLeft', 'ArrowRight', 'Home', 'End'
    ];
  
    // Allow only digits and specified control keys
    return allowedKeys.includes(key);
  }


const stateData = {
    NG: ['Abia', 'Adamawa', 'AkwaIbom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue', 'Borno',
        'CrossRiver', 'Delta', 'Ebonyi', 'Edo','Ekiti', 'Enugu', 'Gombe', 'Imo', 'Jigawa',
        'Kaduna', 'Kano', 'Kastina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa',
        'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyobo', 'Plateau', 'Rivers', 'Sokoto', 
        'Taraba', 'Yobe', 'Zamfara', 'FCT_Abuja'], // Add more states for Nigeria
    US: ["California", "Texas", "New York"] // Add more states for the US
  };
  
  const lgaData = {
    Abia: ["Umuahia North", "Umuahia South", "Ikwuano", "Obioma Ngwa North"],
    Adamawa: ["Yola North", "Yola South", "Ganye", "Jada"],
    AkwaIbom: ["Uyo", "Ikot Ekpene", "Eket", "Oron"],
    Anambra: ["Awka South", "Awka North", "Onitsha North", "Onitsha South"],
    Bauchi: ["Bauchi", "Dass", "Bogoro", "Tafawa Balewa"],
    Bayelsa: ["Yenagoa", "Sagbama", "Southern Ijaw", "Kolokuma/Opokuma"],
    Benue: ["Makurdi", "Gboko", "Otukpo", "Katsina-Ala"],
    Borno: ["Maiduguri", "Bama", "Gwoza", "Kukawa"],
    CrossRiver: ["Calabar South", "Calabar Municipality", "Odukpani", "Akpabuyo"],
    Delta: ["Warri South", "Warri North", "Udu", "Okpe"],
    Ebonyi: ["Abakaliki", "Afikpo North", "Afikpo South", "Ebonyi"],
    Edo: ["Benin City", "Egor", "Oredo", "Ikpoba-Okha"],
    Ekiti: ["Ado Ekiti", "Ikere Ekiti", "Ido Osi", "Ilejemeje"],
    Enugu: ["Enugu East", "Enugu North", "Enugu South", "Igbo Etiti"],
    Gombe: ["Gombe", "Akko", "Balanga", "Dukku"],
    Imo: ["Owerri North", "Owerri South", "Owerri Municipal", "Orlu"],
    Jigawa: ["Dutse", "Ringim", "Malam Madori", "Buji"],
    Kaduna: ["Kaduna North", "Kaduna South", "Igabi", "Zaria"],
    Kano: ["Kano Municipal", "Dala", "Kumbotso", "Tarauni"],
    Kastina: ["Katsina Municipal", "Daura", "Funtua", "Kankara"],
    Kebbi: ["Birnin Kebbi", "Bunza", "Gwandu", "Jega"],
    Kogi: ["Lokoja", "Kogi", "Ijumu", "Idah"],
    Kwara: ["Ilorin South", "Ilorin West", "Ilorin East", "Asa"],
    Lagos: ["Ikeja", "Surulere", "Kosofe", "Mushin"],
    Nasarawa: ["Lafia", "Nasarawa", "Keffi", "Karu"],
    Niger: ["Minna", "Bosso", "Chanchaga", "Agaie"],
    Ogun: ["Abeokuta North", "Abeokuta South", "Ogun Waterside", "Remo North"],
    Ondo: ["Akure North", "Akure South", "Owo", "Ifedore"],
    Osun: ["Osogbo", "Ado-Ekiti West", "Ilesa East", "Ilesa West"],
    Oyo: ["Ibadan", "Ikeja", "Surulere", "Kosofe"],
    Plateau: ["Jos North", "Jos South", "Barkin Ladi", "Bassa"],
    Rivers: ["Port Harcourt", "Obio/Akpor", "Ikwerre", "Oyigbo"],
    Sokoto: ["Sokoto South", "Sokoto North", "Wurno", "Gada"],
    Taraba: ["Jalingo", "Wukari", "Gashaka, Kurmi", "Sardauna"],
    Yobe: ["Damaturu", "Buni Yadi", "Fika", "Guzamala"],
    Zamfara: ["Gusau", "Maradun", "Kaura Namoda", "Shinkafi"],
    FCT_Abuja: ["Gwagwalada", "Katamkpe"],
    California: ["Los Angeles", "San Francisco", "San Diego"], // Add more LGAs for California
    Texas: ["Houston", "Dallas", "Austin"], // Add more LGAs for Texas
    NewYork: ["New York City", "Buffalo", "Rochester"] // Add more LGAs for New York
  };
  
  function populateStates() {
    const countrySelect = document.getElementById("country");
    const stateSelect = document.getElementById("state");
    const selectedCountry = countrySelect.value;
  
    stateSelect.innerHTML = '<option value="">Select State</option>'; // Reset states
  
    if (selectedCountry) {
      stateData[selectedCountry].forEach(state => {
        const option = document.createElement("option");
        option.value = state;
        option.textContent = state;
        stateSelect.appendChild(option);
      });
    }
  }
  
  function populateLGAs() {
    const stateSelect = document.getElementById("state");
    const lgaSelect = document.getElementById("lga");
    const selectedState = stateSelect.value;
  
    lgaSelect.innerHTML = '<option value="">Select LGA</option>'; // Reset LGAs
  
    if (selectedState) {
      lgaData[selectedState].forEach(lga => {
        const option = document.createElement("option");
        option.value = lga;
        option.textContent = lga;
        lgaSelect.appendChild(option);
      });
    }
  }

const form = document.getElementById("shipform");

form.addEventListener("submit", async (event) => {
  event.preventDefault(); // prevents the default submission

  const formdata = new FormData(form);

  const response = await fetch("/profile/address", {
    method: "POST",
    body: formdata,
  });
  const data = await response.json();
  alert(data);
  form.reset();
});