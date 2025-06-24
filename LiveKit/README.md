# LiveKit Voice AI Assistant

This project implements a voice AI assistant using LiveKit Agents, designed specifically for schools in Saudi Arabia. The assistant interacts with users in Arabic and provides information from a school catalog.

## Project Structure

```
LiveKit
├── agent.py          # Main implementation of the voice AI assistant
├── Catalog.py        # Contains data or functions related to the school catalog
├── KMS
│   └── logs          # Directory for storing log files of user interactions
├── requirements.txt  # Lists the dependencies required for the project
└── README.md         # Documentation for the project
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd LiveKit
   ```

2. **Install Dependencies**
   Ensure you have Python installed, then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**
   Create a `.env` file in the root directory and add the necessary environment variables, such as:
   ```
   TAVUS_API_KEY=<your_tavus_api_key>
   ```

## Usage

To run the voice AI assistant, execute the following command:
```bash
python agent.py
```

The assistant will start and be ready to interact with users. It will greet users and provide information based on the school catalog.

## Logging

User interactions and conversations are logged in the `KMS/logs` directory. This helps in tracking user engagement and improving the assistant's responses.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.